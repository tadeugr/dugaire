#!/usr/bin/env python3

""" Import comunity modules. """

import os
import sys
import docker
import json
from click.testing import CliRunner

HERE = os.path.dirname(os.path.realpath(__file__))

""" Import custom modules. """

sys.path.insert(0, f"{HERE}")
import helper

sys.path.insert(1, f"{HERE}/../dugaire")
import dugaire
import info


def test_default():
    cmd = ""
    cmd += "build"

    result = helper.cli(cmd)

    assert len(result) == 12


def test_from_ubuntu_20_04():
    cmd = ""
    cmd += "build --from=ubuntu:20.04"

    result = helper.cli(cmd)

    assert len(result) == 12


def test_from_ubuntu_18_04():
    cmd = ""
    cmd += "build --from=ubuntu:18.04"

    result = helper.cli(cmd)

    assert len(result) == 12


def test_from_ubuntu_16_04():
    cmd = ""
    cmd += "build --from=ubuntu:16.04"

    result = helper.cli(cmd)

    assert len(result) == 12