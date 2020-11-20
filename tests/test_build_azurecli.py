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


def cli(cmd):
    result = CliRunner().invoke(dugaire.cli, cmd.split(" "))
    image_id = result.output.strip()
    return image_id


def docker_run(image_id, cmd):
    client = docker.from_env()
    docker_run_output = client.containers.run(image_id, cmd, auto_remove=True)
    docker_run_output = docker_run_output.decode("utf-8")
    docker_run_output = json.loads(docker_run_output)
    return docker_run_output


def test_from_ubuntu20_04_pkg_latest():

    from_ = "ubuntu:20.04"
    pkg_version = "latest"
    pkg_version_assert = None

    cmd = f"build --from={from_} --with-azurecli={pkg_version}"
    image_id = cli(cmd)
    assert len(image_id) == 12

    docker_run_output = docker_run(image_id, "az version --output=json")

    assert "azure-cli" in docker_run_output


def test_from_ubuntu20_04_pkg_2_14_2():

    from_ = "ubuntu:20.04"
    pkg_version = "2.14.2"

    cmd = f'build --from={from_} --apt=python3-pip --pip3="azure-cli=={pkg_version}"'
    print(cmd)

    image_id = cli(cmd)
    assert len(image_id) == 12

    docker_run_output = docker_run(image_id, "az version --output=json")

    assert pkg_version == docker_run_output["azure-cli"]
