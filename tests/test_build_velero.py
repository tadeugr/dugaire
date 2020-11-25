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


def test_from_ubuntu_20_04_bad_usage():
    invalid_option = "THIS.IS.INVALID"
    cmd = f"build --from=ubuntu:20.04 --with-velero={invalid_option}"
    result = common.cli(cmd)
    assert f'Bad usage --with-velero={invalid_option}' in result

def test_from_ubuntu_20_04_no_kubectl():
    cmd = f"build --from=ubuntu:20.04 --with-velero=1.5.2"
    result = common.cli(cmd)
    assert 'Bad usage --with-velero requires --with-kubectl' in result

def test_from_ubuntu_20_04_pkg_latest():
    cmd = f"build --from=ubuntu:20.04 --with-kubectl=latest --with-velero=latest"
    image_id = common.cli(cmd)
    assert len(image_id) == 12

    docker_run_output = common.docker_run(
        image_id, "kubectl version --client=true --output=json"
    )
    docker_run_output = json.loads(docker_run_output)

    assert "gitVersion" in docker_run_output["clientVersion"]

    docker_run_output = common.docker_run(
        image_id, "velero version --client-only"
    )

    assert "Git commit:" in docker_run_output