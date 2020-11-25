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
import common

def test_from_ubuntu_20_04_pkg_latest():
    cmd = f"build --from=ubuntu:20.04 --with-kubectl=latest"
    image_id = common.cli(cmd)
    assert len(image_id) == 12

    docker_run_output = common.docker_run(
        image_id, "kubectl version --client=true --output=json"
    )
    docker_run_output = json.loads(docker_run_output)

    assert "gitVersion" in docker_run_output["clientVersion"]


def test_from_ubuntu_20_04_pkg_1_18_0():
    pkg_version = "1.18.0"
    cmd = f"build --from=ubuntu:20.04 --with-kubectl={pkg_version}"
    image_id = common.cli(cmd)
    assert len(image_id) == 12

    docker_run_output = common.docker_run(
        image_id, "kubectl version --client=true --output=json"
    )
    docker_run_output = json.loads(docker_run_output)

    f"v{pkg_version}" == docker_run_output["clientVersion"]["gitVersion"]


def test_from_ubuntu_20_04_pkg_1_17_0():
    pkg_version = "1.17.0"
    cmd = f"build --from=ubuntu:20.04 --with-kubectl={pkg_version}"
    image_id = common.cli(cmd)
    assert len(image_id) == 12

    docker_run_output = common.docker_run(
        image_id, "kubectl version --client=true --output=json"
    )
    docker_run_output = json.loads(docker_run_output)

    f"v{pkg_version}" == docker_run_output["clientVersion"]["gitVersion"]


def test_from_ubuntu_20_04_pkg_1_16_0():
    pkg_version = "1.16.0"
    cmd = f"build --from=ubuntu:18.04 --with-kubectl={pkg_version}"
    image_id = common.cli(cmd)
    assert len(image_id) == 12

    docker_run_output = common.docker_run(
        image_id, "kubectl version --client=true --output=json"
    )
    docker_run_output = json.loads(docker_run_output)

    f"v{pkg_version}" == docker_run_output["clientVersion"]["gitVersion"]


def test_from_ubuntu_20_04_pkg_1_15_0():
    pkg_version = "1.15.0"
    cmd = f"build --from=ubuntu:18.04 --with-kubectl={pkg_version}"
    image_id = common.cli(cmd)
    assert len(image_id) == 12

    docker_run_output = common.docker_run(
        image_id, "kubectl version --client=true --output=json"
    )
    docker_run_output = json.loads(docker_run_output)

    f"v{pkg_version}" == docker_run_output["clientVersion"]["gitVersion"]
