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

def test_build_ubuntu1804_apt_pip3_kubectl():

    install_kubectl_version = "1.17.0"

    cmd = ""
    cmd += f"build --from=ubuntu:18.04 --apt=vim,python3-pip --pip3=ansible --with-kubectl={install_kubectl_version}"

    result = CliRunner().invoke(dugaire.cli, cmd.split(" "))
    image_id = result.output.strip()

    assert len(image_id) == 12

    client = docker.from_env()
    docker_run_output = client.containers.run(
        image_id, "kubectl version --client=true --output=json", auto_remove=True
    )
    docker_run_output = docker_run_output.decode("utf-8")
    kubectl_version = json.loads(docker_run_output)
    print(kubectl_version)

    assert (
        f"v{install_kubectl_version}" == kubectl_version["clientVersion"]["gitVersion"]
    )
