#!/usr/bin/env python3

# Import comunity modules.

import os
import sys

# Set module import path.

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, f"{HERE}/../dugaire")

# Import custom modules.

import common

def test_help():
    """
    Run:
    dugaire --help
    """

    result = common.cli("--help")
    assert "CLI tool to build and manage custom Docker images." in result
