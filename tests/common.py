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

import dugaire


def dugaire_cli(cmd):
    """Run click command."""

    print(f"Running: dugaire {cmd}")
    result = CliRunner().invoke(dugaire.cli_, cmd.split(" "))
    result = result.output.strip()
    return result


def docker_run(image_id, cmd):
    """Run docker run command."""

    client = docker.from_env()
    docker_run_output = client.containers.run(image_id, cmd, auto_remove=True)
    docker_run_output = docker_run_output.decode("utf-8")
    return docker_run_output
