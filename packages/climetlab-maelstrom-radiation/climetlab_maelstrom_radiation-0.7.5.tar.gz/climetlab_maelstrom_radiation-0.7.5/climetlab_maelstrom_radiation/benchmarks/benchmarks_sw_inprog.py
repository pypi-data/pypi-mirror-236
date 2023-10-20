#!/usr/bin/env python
# (C) Copyright 2021 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

from time import time

# To hide GPU uncomment
# import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import mantik

import tensorflow as tf
from tensorflow.keras.optimizers import Adam

from .utils import EpochTimingCallback, printstats  # TimingCallback,
from .data import load_train_val_data
from .models import build_cnn, build_fullcnn, build_rnn, load_model
from climetlab_maelstrom_radiation.benchmarks import losses
import horovod.keras as hvd
from deep500.utils import timer_tf as timer
import mlflow


def main(
    batch_size=256,
    epochs=5,
    synthetic_data=False,
    cache=True,
    data_only=False,
    run_no=0,
    model_type="cnn",
    tier=1,
    continue_model="",
    no_recompile=False,
    attention=False,
    inference=False,
    no_tf32=False,
):
    tier_lengths = [None, 133]

    if model_type == "min_cnn":
        minimal = True
    else:
        minimal = False
    if no_tf32:
        tf.config.experimental.enable_tensor_float_32_execution(False)
        print("Turning off TF32 for cnn+attention")
    # Pin GPU to be used to process local rank (one GPU per process)
    gpus = tf.config.experimental.list_physical_devices("GPU")
    print(gpus)
    if gpus:
        # tf.config.experimental.set_visible_devices(gpus[hvd.local_rank()], "GPU")
        tf.config.experimental.set_visible_devices(gpus[0], "GPU")

    print("Getting training/validation data")
    total_start = time()
    train, val = load_train_val_data(
        batch_size=batch_size,
        synthetic_data=synthetic_data,
        cache=cache,
        minimal=minimal,
        tier=tier,
        shard_num=1,# hvd.size(),
        shard_idx=0,# hvd.local_rank(),
    )
    # train = train.take(10)
    model = build_fullcnn(
        train.element_spec[0],
        train.element_spec[1],
        attention=attention,
    )
    loss = {"hr_sw": "mae", "sw": losses.top_scaledflux_mae}
    weights = {"hr_sw": 10 ** (-1), "sw": 1}
    lr = 2 * 10 ** (-4)

        # Horovod: add Horovod Distributed Optimizer.
    opt = Adam(lr * batch_size / 256 )# * hvd.size())
        # opt = hvd.DistributedOptimizer(opt)

    model.compile(
        loss=loss,
        metrics={"hr_sw": ["mse", "mae"], "sw": ["mse", "mae"]},
        loss_weights=weights,
        optimizer=opt,
        # experimental_run_tf_function=False,
    )
 
    model.summary()
    print("here we go")

    logfile = f"training_{model_type}_{run_no}.log"
    callbacks = [
    ]
    tmr = timer.CPUGPUTimer()
    # tmr.start(timer.TimeType.EPOCH)
    callbacks.append(timer.TimerCallback(tmr, gpu=True))# ,length=133))
    
 
def benchmarks_sw_wrapper():
    import argparse

    parser = argparse.ArgumentParser(description="Run benchmark")
    parser.add_argument(
        "--synthetic_data",
        help="Use synthetic dataset for pipeline testing",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--data_only",
        help="Only load data.",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--attention",
        help="Use attention in CNN.",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--tier",
        help="Dataset version",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--inference",
        help="Run inference on test set",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument("--batch", type=int, default=512)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--model", type=str, default="min_cnn")
    parser.add_argument("--continue_model", type=str, default="")
    parser.add_argument(
        "--no_recompile",
        help="Continue model without recompling",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--nocache",
        help="Don't cache dataset",
        action="store_const",
        const=True,
        default=False,
    )

    parser.add_argument(
        "--notf32",
        help="Don't use TensorFloat32",
        action="store_const",
        const=True,
        default=False,
    )

    parser.add_argument("--runno", type=int)

    args = parser.parse_args()
    main(
        batch_size=args.batch,
        epochs=args.epochs,
        synthetic_data=args.synthetic_data,
        cache=(not args.nocache),
        data_only=args.data_only,
        run_no=args.runno,
        model_type=args.model,
        tier=args.tier,
        continue_model=args.continue_model,
        no_recompile=args.no_recompile,
        attention=args.attention,
        inference=args.inference,
        no_tf32=args.notf32,
    )
    
if __name__ == "__main__":
    benchmarks_sw_wrapper()
