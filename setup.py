#!/usr/bin/env python3

""" Import comunity modules. """
import os
import sys
from setuptools import find_packages, setup

""" Import custom modules. """

# The directory containing this file
HERE = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(1, f"{HERE}/dugaire")

from common import module as common

# REAME content
README = open(os.path.join(HERE, "README.md")).read()

setup(
    name=common.info.get_prog_name(),
    version=common.info.get_version(),
    description="Build Docker images with custom packages for local development, testing and daily tasks.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tadeugr/dugaire",
    author="Tadeu Granemann",
    license="Apache License, Version 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "docker==4.3.1",
        "click==7.1.2",
        "Jinja2==2.11.2",
        "click-completion==0.5.2",
    ],
    entry_points={"console_scripts": ["dugaire=dugaire.dugaire:main"]},
)
