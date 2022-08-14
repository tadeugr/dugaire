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

import common


def test_from_ubuntu_20_04_bad_usage():
    cmd = f"build --from=ubuntu:20.04 --with-velero=this.is.invalid"
    result = common.cli(cmd)
    assert f"Invalid value" in result


def test_from_ubuntu_20_04_pkg_latest():
    cmd = f"build --from=ubuntu:20.04 --with-kubectl=latest --with-velero=latest"
    image_id = common.cli(cmd)
    assert len(image_id) == 12

    docker_run_output = common.docker_run(
        image_id, "kubectl version --client=true --output=json"
    )
    docker_run_output = json.loads(docker_run_output)

    assert "gitVersion" in docker_run_output["clientVersion"]

    docker_run_output = common.docker_run(image_id, "velero version --client-only")

    assert "Git commit:" in docker_run_output


def test_from_ubuntu_20_04_pkg_version():
    kubectl_version = "1.17.0"
    velero_version = "1.5.2"
    cmd = f"build --from=ubuntu:20.04 --with-kubectl={kubectl_version} --with-velero={velero_version}"
    image_id = common.cli(cmd)
    assert len(image_id) == 12

    docker_run_output = common.docker_run(
        image_id, "kubectl version --client=true --output=json"
    )
    docker_run_output = json.loads(docker_run_output)

    f"v{kubectl_version}" == docker_run_output["clientVersion"]["gitVersion"]

    docker_run_output = common.docker_run(image_id, "velero version --client-only")

    assert f"Version: v{velero_version}" in docker_run_output
