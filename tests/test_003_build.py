#!/usr/bin/env python3

# Import comunity modules.

import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, f"{HERE}/../dugaire")

# Import custom modules.

import dugaire
from pkg.app import app
import common

_BUILT_IMAGES = []


def test_build_default_and_remove():
    """
    Run:
    dugaire build
    dugaire rmi <image ID>
    """

    image_id = common.dugaire_cli("build")
    assert 12 == len(image_id)

    result = common.dugaire_cli(f"rmi {image_id}")
    assert f"Deleted: {image_id}" in result


def test_build_pip3_and_remove():
    """
    Run:
    dugaire build --pip3=rich
    dugaire rmi <image ID>
    """

    image_id = common.dugaire_cli("build --pip3=rich")
    assert 12 == len(image_id)

    docker_run_output = common.docker_run(image_id, "python3 -m rich")
    assert "Thanks for trying out Rich" in docker_run_output

    result = common.dugaire_cli(f"rmi {image_id}")
    assert f"Deleted: {image_id}" in result


def test_build_default_and_remove_multiple():
    """
    Run:
    dugaire build --apt=curl
    dugaire build --apt=vim
    dugaire rmi <image ID 001> <image ID 002>
    """

    image_id_001 = common.dugaire_cli("build --apt=curl")
    assert 12 == len(image_id_001)

    image_id_002 = common.dugaire_cli("build --apt=vim")
    assert 12 == len(image_id_002)

    result = common.dugaire_cli(f"rmi {image_id_001} {image_id_002}")
    assert f"Deleted: {image_id_001}" in result
    assert f"Deleted: {image_id_002}" in result


def test_build_default_and_remove_all():
    """
    Run:
    dugaire build --apt=wget
    dugaire build --apt=nano
    dugaire rmi all
    """

    image_id_001 = common.dugaire_cli("build --apt=wget")
    assert 12 == len(image_id_001)

    image_id_002 = common.dugaire_cli("build --apt=nano")
    assert 12 == len(image_id_002)

    result = common.dugaire_cli(f"rmi all")
    assert f"Deleted: {image_id_001}" in result
    assert f"Deleted: {image_id_002}" in result
