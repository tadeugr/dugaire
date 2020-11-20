#!/usr/bin/env python3

""" Import comunity modules. """

import os
import sys
import docker
import json
from click.testing import CliRunner

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, f"{HERE}/../dugaire")

""" Import custom modules. """

import dugaire
import info

def test_build_latest():
    cmd = ""
    cmd += "build --with-azurecli=latest"

    result = CliRunner().invoke(dugaire.cli, cmd.split(" "))
    output = result.output.strip()

    assert len(output) == 12