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


def test_version_parameter():
    """Test command: dugaire --version"""

    result = common.cli("--version")
    info_version = my_app.get_version()
    assert info_version == result


def test_version_command():
    """Test command: dugaire version"""

    result = common.cli("version")
    info_version = my_app.get_version()
    assert info_version == result
