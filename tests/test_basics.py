#!/usr/bin/env python3

""" Import comunity modules. """

import os
import sys
from click.testing import CliRunner

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, f"{HERE}/../dugaire")

""" Import custom modules. """

import dugaire
import info


def test_help():

    cmd = ""
    cmd += "--help"

    result = CliRunner().invoke(dugaire.cli, cmd.split(" "))
    output = result.output.strip()

    assert f"Usage: cli [OPTIONS] COMMAND [ARGS]" in output


def test_version():

    cmd = ""
    cmd += "--version"

    result = CliRunner().invoke(dugaire.cli, cmd.split(" "))
    output = result.output.strip()

    info_version = info.get_version()
    info_prog_name = info.get_prog_name()

    assert f"{info_prog_name}, version {info_version}" == output
