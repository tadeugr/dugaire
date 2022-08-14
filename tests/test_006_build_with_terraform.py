#!/usr/bin/env python3

# Import comunity modules.

import os
import sys
import json

# Set module import path.

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, f"{HERE}/../dugaire")

# Import custom modules.

import common


def test_from_ubuntu_20_04_with_terraform_latest():
    """
    Run:
    dugaire build --with-terraform=latest
    """

    cmd = f"build --with-terraform=latest"
    image_id = common.dugaire_cli(cmd)
    assert len(image_id) == 12

    docker_run_output = common.docker_run(
        image_id, "terraform --version -json"
    )
    docker_run_output = json.loads(docker_run_output)

    assert "terraform_version" in docker_run_output


def test_from_ubuntu_20_04_with_terraform_0_15_5():
    """
    Run:
    dugaire build --with-terraform=0.15.5
    """

    cmd = f"build --with-terraform=0.15.5"
    image_id = common.dugaire_cli(cmd)
    assert len(image_id) == 12

    docker_run_output = common.docker_run(
        image_id, "terraform --version -json"
    )
    docker_run_output = json.loads(docker_run_output)

    assert "0.15.5" == docker_run_output["terraform_version"]