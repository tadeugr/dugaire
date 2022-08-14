#!/usr/bin/env python3

""" Import comunity modules. """
import os
import sys
from setuptools import find_packages, setup

""" Import custom modules. """

# The directory containing this file
HERE = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(1, f"{HERE}/dugaire")

from pkg.my_app import my_app

# REAME content
README = open(os.path.join(HERE, "README.md")).read()
REQUIREMENTS = open(os.path.join(HERE, "requirements.txt")).read().splitlines()

setup(
    name=my_app.get_prog_name(),
    version=my_app.get_version(),
    description="Build Docker images with custom packages for local development, testing and daily tasks.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tadeugr/dugaire",
    author="Tadeu Granemann",
    license="Apache License, Version 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[REQUIREMENTS],
    entry_points={"console_scripts": ["dugaire=dugaire.dugaire:main"]},
)
