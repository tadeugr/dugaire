#!/usr/bin/env python3

# Import comunity modules.

import os
import sys
from click.testing import CliRunner

# Set module import path.

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, f"{HERE}/../dugaire")

# Import custom modules.

from pkg.app import app
import common


def test_version_parameter():
    """
    Run:
    dugaire --version
    """

    result = common.dugaire_cli("--version")
    info_version = app.get_version()
    assert info_version == result


def test_version_command():
    """
    Run:
    dugaire version
    """

    result = common.dugaire_cli("version")
    info_version = app.get_version()
    assert info_version == result
