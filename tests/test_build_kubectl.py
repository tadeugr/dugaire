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


def test_from_ubuntu_20_04_pkg_latest():
    cmd = f"build --from=ubuntu:20.04 --with-kubectl=latest"
    image_id = cli(cmd)
    assert len(image_id) == 12

    docker_run_output = docker_run(
        image_id, "kubectl version --client=true --output=json"
    )

    assert "gitVersion" in docker_run_output["clientVersion"]


def test_from_ubuntu_20_04_pkg_1_18_0():
    pkg_version = "1.18.0"
    cmd = f"build --from=ubuntu:20.04 --with-kubectl={pkg_version}"
    image_id = cli(cmd)
    assert len(image_id) == 12

    docker_run_output = docker_run(
        image_id, "kubectl version --client=true --output=json"
    )

    f"v{pkg_version}" == docker_run_output["clientVersion"]["gitVersion"]


def test_from_ubuntu_20_04_pkg_1_17_0():
    pkg_version = "1.17.0"
    cmd = f"build --from=ubuntu:20.04 --with-kubectl={pkg_version}"
    image_id = cli(cmd)
    assert len(image_id) == 12

    docker_run_output = docker_run(
        image_id, "kubectl version --client=true --output=json"
    )

    f"v{pkg_version}" == docker_run_output["clientVersion"]["gitVersion"]


def test_from_ubuntu_20_04_pkg_1_16_0():
    pkg_version = "1.16.0"
    cmd = f"build --from=ubuntu:18.04 --with-kubectl={pkg_version}"
    image_id = cli(cmd)
    assert len(image_id) == 12

    docker_run_output = docker_run(
        image_id, "kubectl version --client=true --output=json"
    )

    f"v{pkg_version}" == docker_run_output["clientVersion"]["gitVersion"]


def test_from_ubuntu_20_04_pkg_1_15_0():
    pkg_version = "1.15.0"
    cmd = f"build --from=ubuntu:18.04 --with-kubectl={pkg_version}"
    image_id = cli(cmd)
    assert len(image_id) == 12

    docker_run_output = docker_run(
        image_id, "kubectl version --client=true --output=json"
    )

    f"v{pkg_version}" == docker_run_output["clientVersion"]["gitVersion"]
