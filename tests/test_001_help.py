#!/usr/bin/env python3

""" Import comunity modules. """

import os
import sys
from click.testing import CliRunner

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, f"{HERE}/../dugaire")

""" Import custom modules. """

import dugaire
from pkg.my_app import my_app
import common


def test_help():
    """Test command: dugaire --version"""

    result = common.cli("--help")
    assert "CLI tool to build and manage custom Docker images." in result
