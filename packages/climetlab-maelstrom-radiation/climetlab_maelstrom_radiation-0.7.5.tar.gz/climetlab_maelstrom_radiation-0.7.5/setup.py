#!/usr/bin/env python
# (C) Copyright 2021 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#


import io
import os

import setuptools


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return io.open(file_path, encoding="utf-8").read()


package_name = "climetlab_maelstrom_radiation"

version = None
init_py = os.path.join(package_name.replace("-", "_"), "__init__.py")
for line in read(init_py).split("\n"):
    if line.startswith("__version__"):
        version = line.split("=")[-1].strip()[1:-1]
assert version


extras_require = {}

setuptools.setup(
    name=package_name,
    version=version,
    description="A dataset plugin for climetlab for the dataset maelstrom-radiation.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Matthew Chantry",
    author_email="matthew.chantry@ecmwf.int",
    url="https://git.ecmwf.int/projects/MLFET/repos/maelstrom-radiation",
    license="Apache License Version 2.0",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["climetlab>=0.9.1", "tensorflow>=2.0.0"],
    extras_require=extras_require,
    zip_safe=True,
    entry_points={
        "climetlab.datasets": [
            "maelstrom-radiation = climetlab_maelstrom_radiation.radiation:radiation",
            "maelstrom-radiation-tf = climetlab_maelstrom_radiation.radiation_tf:radiation_tf",
        ],
        "console_scripts": ["radiation-benchmarks-sw = climetlab_maelstrom_radiation.benchmarks.benchmarks_sw:benchmarks_sw_wrapper",
                            "radiation-inference-sw =  climetlab_maelstrom_radiation.benchmarks.benchmarks_sw_inference:sw_inference_wrapper",
                            "radiation-benchmarks-lw = climetlab_maelstrom_radiation.benchmarks.benchmarks_lw:benchmarks_lw_wrapper",
                            "radiation-inference-lw =  climetlab_maelstrom_radiation.benchmarks.benchmarks_lw_inference:lw_inference_wrapper",
        ],
    },
    keywords="meteorology",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
    ],
)
