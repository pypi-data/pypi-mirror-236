#!/usr/bin/env python
# (C) Copyright 2021 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import numpy as np
from .data import norms
import tensorflow as tf
from tensorflow import nn
from tensorflow.keras.layers import (
    Input,
    Conv1D,
    RepeatVector,
    ZeroPadding1D,
)
from tensorflow.keras.layers import (
    Cropping1D,
    Concatenate,
    Multiply,
    Flatten,
    Dense,
    GRU,
    LSTM,
)
from tensorflow.keras.models import Model
from .layers import TopFlux, rnncolumns, HRLayer, rnncolumns_old, AddHeight
from .losses import top_scaledflux_mse, top_scaledflux_mae

activations = {'swish' : nn.swish,
               'tanh' : nn.tanh,
           }

def load_model(model_path):
    custom_objects = {
        "top_scaledflux_mse": top_scaledflux_mse,
        "top_scaledflux_mae": top_scaledflux_mae,
        "rnncolumns": rnncolumns,
        "AddHeight": AddHeight,
    }
    return tf.keras.models.load_model(model_path, custom_objects=custom_objects)


def build_cnn(
    input_shape,
    output_shape,
    kernel_width=5,
    conv_filters=64,
    dilation_rates=[1, 2, 4, 8, 16],
    conv_layers=6,
    flux_layers=3,
    flux_filters=8,
    flux_width=32,
    dl_test=False,
):
    inputs = {}

    # Inputs are a bit messy, in the next few lines we create the input shapes,
    for k in input_shape.keys():
        inputs[k] = Input(input_shape[k].shape[1:], name=k)

    # Calculate the incoming solar radiation before it is normalised.
    in_solar = inputs["sca_inputs"][..., 1:2] * inputs["sca_inputs"][..., -1:]
    # Pressure needs to be un-normalised.
    hl_p = inputs["pressure_hl"]

    # Normalise them by the columnar-maxes
    normed = {}
    for i, k in enumerate(input_shape.keys()):
        normed[k] = inputs[k] / tf.constant(norms[k])

    # and repeat or reshape them so they all have 138 vertical layers
    rep_sca = RepeatVector(138)(normed["sca_inputs"])
    col_inp = ZeroPadding1D(padding=(1, 0))(normed["col_inputs"])
    inter_inp = ZeroPadding1D(padding=(1, 1))(normed["inter_inputs"])
    all_col = Concatenate(axis=-1)([rep_sca, col_inp, normed["hl_inputs"], inter_inp])

    # Use dilation to allow information to propagate faster through the vertical.
    for drate in dilation_rates:
        all_col = Conv1D(
            filters=conv_filters,
            kernel_size=kernel_width,
            dilation_rate=drate,
            padding="same",
            data_format="channels_last",
            activation=nn.swish,
        )(all_col)
    # Regular conv layers
    for i in range(conv_layers):
        all_col = Conv1D(
            conv_filters,
            kernel_size=kernel_width,
            strides=1,
            padding="same",
            data_format="channels_last",
            activation=nn.swish,
        )(all_col)

    # Predict single output, the heating rate.
    sw = Conv1D(
        filters=1,
        padding="same",
        kernel_size=kernel_width,
        data_format="channels_last",
        activation="linear",
    )(all_col)

    # Crop the bottom value to make output correct size.
    # Perhaps you can think of a better solution?
    sw_hr = Cropping1D((0, 1), name="hr_sw")(sw)

    # Reduce the number of features
    flux_col = Conv1D(
        filters=flux_filters,
        padding="same",
        kernel_size=kernel_width,
        activation=nn.swish,
    )(all_col)
    flux_col = Flatten()(flux_col)
    swf = Concatenate(axis=-1)([flux_col, normed["sca_inputs"]])
    # Add a few dense layers, plus the input scalars
    for i in range(flux_layers):
        swf = Dense(flux_width, activation=nn.swish)(swf)
    swf = Dense(2, activation="sigmoid")(swf)
    swf = Multiply()([swf, in_solar])
    swf = TopFlux(name="sw")([swf, sw_hr, hl_p])

    # Dictionary of outputs
    output = {"hr_sw": sw_hr, "sw": swf}

    if dl_test:
        from .dummy_model import DummyModel as Model
    else:
        from tensorflow.keras import Model

    model = Model(inputs, output)
    return model


def build_rnn(
    inp_spec,
    outp_spec,
    nneur=64,
    hr_loss=True,
    activ_last="sigmoid",
    activ0="linear",
    dl_test=False,
    lstm=True,
):
    #Assume inputs have the order
    #scalar, column, hl, inter, pressure_hl
    kw = 5
    all_inp = []
    for k in inp_spec.keys():
        all_inp.append(Input(inp_spec[k].shape[1:],name=k))

    scalar_inp = all_inp[0]
    lay_inp = all_inp[1]
    hl_inp = all_inp[2]
    inter_inp = all_inp[3]
    hl_p = all_inp[-1]

    # inputs we need:
    #  - layer inputs ("lay_inp"), which are the main RNN sequential input
    #     -- includes repeated mu0, t_lay, and log(p_lay)
    #  - albedos, fed to a dense layer whose output is concatenated with the initial
    #             RNN output sequence (137) to get to half-level outputs (138)

    # extract scalar variables we need
    cos_sza = scalar_inp[:,1]
    albedos = scalar_inp[:,2:14]
    solar_irrad = scalar_inp[:,-1]   # not needed as input when predicting scaled flux

    overlap_param = ZeroPadding1D(padding=(1,1))(inter_inp)

    # lay_inp = rnncolumns(colnorms=xcoeffs,name='procCol')(lay_inp,hl_inp,cos_sza)
    lay_inp = rnncolumns(name='procCol')([lay_inp,hl_inp,cos_sza])

    # 2. OUTPUTS
    # Outputs are the raw fluxes scaled by incoming flux
    ny = 2
    # incoming flux from inputs
    incflux = Multiply()([cos_sza, solar_irrad])
    incflux = tf.expand_dims(tf.expand_dims(incflux,axis=1),axis=2)

    # hidden0,last_state = layers.SimpleRNN(nneur,return_sequences=True,return_state=True)(inputs)
    if lstm:
        rnnlayer = LSTM
        hidden0,last_state,last_memory = rnnlayer(nneur,return_sequences=True,
                                      return_state=True,name="RNN1")(lay_inp)
        last_state = tf.concat([last_state,last_memory],axis=-1)
    else:
        rnnlayer = GRU
        hidden0,last_state = rnnlayer(nneur,return_sequences=True,
                                      return_state=True,name="RNN1")(lay_inp)

    last_state_plus_albedo =  tf.concat([last_state,albedos],axis=1)

    mlp_surface_outp = Dense(nneur, activation=activ0,name='dense_surface')(last_state_plus_albedo)

    hidden0_lev = tf.concat([hidden0,tf.reshape(mlp_surface_outp,[-1,1,nneur])],axis=1)

    # !! OVERLAP PARAMETER !! added here as an additional feature to the whole sequence
    hidden0_lev = tf.concat([hidden0_lev, overlap_param],axis=2)

    if lstm:
        mlp_surface_outp2 = Dense(nneur, activation=activ0,name='dense_surface2')(last_state_plus_albedo)
        init_state = [mlp_surface_outp,mlp_surface_outp2]
    else:
        init_state = mlp_surface_outp
    hidden1 = rnnlayer(nneur,return_sequences=True,
                       go_backwards=True)(hidden0_lev, initial_state=init_state)

    hidden1 = tf.reverse(hidden1,axis=[1])

    # at least before I had better results when concatinating hidden0 and hidden1
    hidden_concat  = tf.concat([hidden0_lev,hidden1],axis=2)

    # Third and final RNN layer
    hidden2 = rnnlayer(nneur,return_sequences=True)(hidden_concat)#,#
    # flux_sw = TimeDistributed(Dense(ny, activation=activ_last))(hidden2)
    flux_sw = Conv1D(ny, kernel_size = 1, activation=activ_last,
                     name='sw_denorm'
    )(hidden2)

    flux_sw = Multiply(name='sw')([flux_sw, incflux])
    hr_sw = HRLayer(name='hr_sw')([flux_sw, hl_p])

    outputs = {'sw':flux_sw, 'hr_sw':hr_sw}

    if dl_test:
        from .dummy_model import DummyModel as Model
    else:
        from tensorflow.keras import Model
    model = Model(all_inp, outputs)
    return model

def build_fullcnn(
    inp_shape,
    out_shape,
    conv_filters=64,
    dilation_rates=[1, 2, 4, 8, 16],
    conv_layers=5,
    kernel_width=5,
    activation="swish",
    attention=False,
    num_heads=8,
    dl_test=False,
):
    # Assume inputs have the order
    # scalar, column, hl, inter, pressure_hl
    all_inp = []
    for k in inp_shape.keys():
        print(k)
        all_inp.append(Input(inp_shape[k].shape[1:], name=k))
        if k == "sca_inputs":
            in_solar = all_inp[-1][..., 1:2] * all_inp[-1][..., -1:]
    hl_p = all_inp[-1]
    first_layer = all_inp

    second_layer = []
    for i, k in enumerate(inp_shape.keys()):
        second_layer.append(first_layer[i] / tf.constant(norms[k]))

    # Reshape inputs ready for merging.
    rep_sca = RepeatVector(138)(second_layer[0])
    col_inp = ZeroPadding1D(padding=(1, 0))(second_layer[1])
    inter_inp = ZeroPadding1D(padding=(1, 1))(second_layer[3])
    # Merge all inputs
    all_col = Concatenate(axis=-1)([rep_sca, col_inp, second_layer[2], inter_inp])

    if attention:
        print("Not using dilation with attention")
        dilation_rates = [1 for i in dilation_rates]
    for drate in dilation_rates:
        all_col = Conv1D(
            filters=conv_filters,
            kernel_size=kernel_width,
            dilation_rate=drate,
            padding="same",
            activation=activations[activation],
        )(all_col)

    if attention:
        key_dim = conv_filters // num_heads
        all_col = tf.keras.layers.MultiHeadAttention(
            num_heads=num_heads, key_dim=key_dim, name="attention_1"
        )(all_col, all_col)

    for i in range(conv_layers):
        all_col = Conv1D(
            filters=conv_filters,
            kernel_size=kernel_width,
            dilation_rate=1,
            padding="same",
            activation=activations[activation],
        )(all_col)

    if attention:
        key_dim = conv_filters // num_heads
        all_col = tf.keras.layers.MultiHeadAttention(
            num_heads=num_heads, key_dim=key_dim, name="attention_2"
        )(all_col, all_col)

    outputs = {}
    if "lw" in out_shape.keys():
        lwf = Conv1D(
            filters=2,
            padding="same",
            kernel_size=kernel_width,
            activation="softplus",
            name="lw",
        )(all_col)
        outputs["lw"] = lwf

        if "hr_lw" in out_shape.keys():
            outputs["hr_lw"] = HRLayer(name="hr_lw")([lwf, hl_p])

    if "sw" in out_shape.keys():
        swf = Conv1D(
            filters=2,
            padding="same",
            kernel_size=kernel_width,
            activation="sigmoid",
            name="swm1",
        )(all_col)
        swf = Multiply(name="sw")([swf, in_solar])
        outputs["sw"] = swf

        if "hr_sw" in out_shape.keys():
            outputs["hr_sw"] = HRLayer(name="hr_sw")([swf, hl_p])
    if dl_test:
        from .dummy_model import DummyModel as Model
    else:
        from tensorflow.keras import Model
    model = Model(all_inp, outputs)
    return model

def build_rnn_lw(inp_spec,outp_spec, nneur=64, hr_loss=True,
           max_norm = True, activ_last = 'sigmoid',
           lstm = True, dense_middle = False, activ = 'swish',
):
    #Assume inputs have the order
    #scalar, column, hl, inter, pressure_hl
    kw = 5
    all_inp = []
    for k in inp_spec.keys():
        all_inp.append(Input(inp_spec[k].shape[1:],name=k))

    scalar_inp = all_inp[0]
    lay_inp = all_inp[1]
    hl_inp = all_inp[2]
    inter_inp = all_inp[3]
    hl_p = all_inp[-1]

    if max_norm:
        normed_scalar = scalar_inp/tf.constant(norms['sca_inputs'])

    mlp_surface_outp = Dense(nneur, activation=activ,name='dense_surface')(normed_scalar)
    flux_scale = Dense(32, activation='softplus',name='dense_scale1')(normed_scalar)
    flux_scale = Dense(1, activation='softplus',name='dense_scale2')(flux_scale)
    flux_scale = tf.expand_dims(flux_scale,axis=-1)

    # extract scalar variables we need
    cos_sza = scalar_inp[:,1]
    albedos = scalar_inp[:,2:14]
    solar_irrad = scalar_inp[:,-1]   # not needed as input when predicting scaled flux

    overlap_param = ZeroPadding1D(padding=(1,1))(inter_inp)

    lay_inp = rnncolumns(name='procCol')([lay_inp,hl_inp,cos_sza])

    # 2. OUTPUTS
    # Outputs are the raw fluxes scaled by incoming flux
    # incoming flux from inputs
    if lstm:
        rnnlayer = LSTM
        mlp_surface_outp2 = Dense(nneur, activation=activ,name='dense_surface2')(normed_scalar)
        init_state = [mlp_surface_outp,mlp_surface_outp2]
        hidden0,up_state,up_state2 = rnnlayer(nneur,return_sequences=True,
                                              go_backwards=True,
                                              return_state=True,
                                              name="RNN_Up")(lay_inp,
                                                   initial_state=init_state)
    else:
        rnnlayer = GRU
        init_state = mlp_surface_outp

        hidden0,up_state = rnnlayer(nneur,return_sequences=True,
                                    go_backwards=True,
                                    return_state=True,
                                    name="RNN_Up")(lay_inp,
                                                   initial_state=init_state)

    hidden0 = tf.reverse(hidden0,axis=[1])

    hidden0_lev = tf.concat([hidden0,tf.reshape(mlp_surface_outp,[-1,1,nneur])],axis=1)

    # !! OVERLAP PARAMETER !! added here as an additional feature to the whole sequence
    hidden0_lev = tf.concat([hidden0_lev, overlap_param],axis=2)

    if dense_middle:
        up_state = Dense(nneur,activation=activ)(up_state)
        if lstm:
            up_state2 = Dense(nneur,activation=activ)(up_state2)
    if lstm:
        up_state = [up_state,up_state2]


    hidden1 = rnnlayer(nneur,return_sequences=True,
                  name="RNN_Dwn")(hidden0_lev,
                                  initial_state=up_state)

    hidden_concat  = tf.concat([hidden0_lev,hidden1],axis=2)

    flux_sw = Conv1D(2, kernel_size = 1, activation=activ_last,
                     name='lw_denorm'
    )(hidden_concat)
    flux_sw = Multiply(name='lw')([flux_sw, flux_scale])

    hr_sw = HRLayer(name='hr_lw')([flux_sw, hl_p])

    outputs = {'lw':flux_sw, 'hr_lw':hr_sw}
    return Model(all_inp, outputs)
