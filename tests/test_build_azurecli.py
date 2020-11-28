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

sys.path.insert(0, f"{HERE}")
import helper

sys.path.insert(1, f"{HERE}/../dugaire")
import dugaire
import info


def test_from_default_pkg_latest():

    pkg_version = "latest"

    cmd = f"build --with-azurecli={pkg_version}"
    image_id = helper.cli(cmd)
    assert len(image_id) == 12

    docker_run_output = helper.docker_run(image_id, "az version --output=json")

    assert "azure-cli" in docker_run_output


def test_from_ubuntu20_04_pkg_2_14_2():

    from_ = "ubuntu:20.04"
    pkg_version = "2.14.2"

    cmd = f'build --from={from_} --pip3="azure-cli=={pkg_version}"'

    image_id = helper.cli(cmd)
    assert len(image_id) == 12

    docker_run_output = helper.docker_run(image_id, "az version --output=json")
    docker_run_output = json.loads(docker_run_output)

    assert pkg_version == docker_run_output["azure-cli"]

def test_from_ubuntu18_04_pkg_2_13_0():

    from_ = "ubuntu:18.04"
    pkg_version = "2.13.0"

    cmd = f'build --from={from_} --pip3="azure-cli=={pkg_version}"'

    image_id = helper.cli(cmd)
    assert len(image_id) == 12

    docker_run_output = helper.docker_run(image_id, "az version --output=json")
    docker_run_output = json.loads(docker_run_output)

    assert pkg_version == docker_run_output["azure-cli"]