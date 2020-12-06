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


def test_from_ubuntu_20_04_bad_usage():
    invalid_option = "THIS.IS.INVALID"
    cmd = f"build --from=ubuntu:20.04 --with-velero={invalid_option}"
    result = helper.cli(cmd)
    assert f"Bad usage --with-velero={invalid_option}" in result


def test_from_ubuntu_20_04_no_kubectl():
    cmd = f"build --from=ubuntu:20.04 --with-velero=1.5.2"
    result = helper.cli(cmd)
    assert "--with-velero requires --with-kubectl" in result


def test_from_ubuntu_20_04_pkg_latest():
    cmd = f"build --from=ubuntu:20.04 --with-kubectl=latest --with-velero=latest"
    image_id = helper.cli(cmd)
    assert len(image_id) == 12

    docker_run_output = helper.docker_run(
        image_id, "kubectl version --client=true --output=json"
    )
    docker_run_output = json.loads(docker_run_output)

    assert "gitVersion" in docker_run_output["clientVersion"]

    docker_run_output = helper.docker_run(image_id, "velero version --client-only")

    assert "Git commit:" in docker_run_output


def test_from_ubuntu_20_04_pkg_version():
    kubectl_version = "1.17.0"
    velero_version = "1.5.2"
    cmd = f"build --from=ubuntu:20.04 --with-kubectl={kubectl_version} --with-velero={velero_version}"
    image_id = helper.cli(cmd)
    assert len(image_id) == 12

    docker_run_output = helper.docker_run(
        image_id, "kubectl version --client=true --output=json"
    )
    docker_run_output = json.loads(docker_run_output)

    f"v{kubectl_version}" == docker_run_output["clientVersion"]["gitVersion"]

    docker_run_output = helper.docker_run(image_id, "velero version --client-only")

    assert f"Version: v{velero_version}" in docker_run_output
