#!/usr/bin/env python3

# Import comunity modules.

import os
import sys
import docker
import json
from click.testing import CliRunner

# Set module import path.

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, f"{HERE}/../dugaire")

# Import custom modules.

import common
from pkg.cli import cli


def test_from_ubuntu20_04_a_package():
    """
    Run:
    dugaire build --from=ubuntu:20.04 --apt=python3-pip --pip3=pytest
    """

    from_ = "ubuntu:20.04"
    pkg = "pytest"

    cmd = f"build --from={from_} --apt=python3-pip --pip3={pkg}"
    image_id = common.dugaire_cli(cmd)
    assert len(image_id) == 12

    docker_run_output = common.docker_run(image_id, "pytest --version")
    docker_run_output_split = [word.strip() for word in docker_run_output.split(" ")]

    assert 2 == len(docker_run_output_split)
    assert "pytest" in docker_run_output_split[0]
    assert cli.is_version_valid(None, None, docker_run_output_split[1])


def test_from_ubuntu20_04_multiple_packages_omit_apt():
    """
    Run:
    dugaire build --from=ubuntu:20.04 --pip3=celery,pytest
    """

    from_ = "ubuntu:20.04"
    pkg = "celery,pytest"

    cmd = f"build --from={from_} --pip3={pkg}"
    image_id = common.dugaire_cli(cmd)
    assert len(image_id) == 12

    docker_run_output = common.docker_run(image_id, "pytest --version")
    docker_run_output_split = [word.strip() for word in docker_run_output.split(" ")]

    assert 2 == len(docker_run_output_split)
    assert "pytest" in docker_run_output_split[0]
    assert cli.is_version_valid(None, None, docker_run_output_split[1])

    docker_run_output = common.docker_run(image_id, "python3 -c 'import celery'")

    assert "" == docker_run_output
