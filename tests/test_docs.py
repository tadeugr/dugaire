#!/usr/bin/env python3

""" Import comunity modules. """

import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, f"{HERE}/../docs")

""" Import custom modules. """

import make_readme


def test_make_readme():

    result = make_readme.make()

    assert f"Base image (used in Dockerfile FROM)" in result
