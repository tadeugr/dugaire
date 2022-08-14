#!/usr/bin/env python3

""" Import comunity modules. """

import os
import sys
from click.testing import CliRunner

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, f"{HERE}/../dugaire")

""" Import custom modules. """

import dugaire
from pkg.my_app import my_app
import common

_BUILT_IMAGES = []


def test_build_default_and_remove():

    image_id = common.cli("build")
    assert 12 == len(image_id)

    result = common.cli(f"rmi {image_id}")
    assert f"Deleted: {image_id}" in result


def test_build_default_and_remove_multiple():

    image_id_001 = common.cli("build --apt=curl")
    assert 12 == len(image_id_001)

    image_id_002 = common.cli("build --apt=vim")
    assert 12 == len(image_id_002)

    result = common.cli(f"rmi {image_id_001} {image_id_002}")
    assert f"Deleted: {image_id_001}" in result
    assert f"Deleted: {image_id_002}" in result


def test_build_default_and_remove_all():

    image_id_001 = common.cli("build --apt=wget")
    assert 12 == len(image_id_001)

    image_id_002 = common.cli("build --apt=nano")
    assert 12 == len(image_id_002)

    result = common.cli(f"rmi all")
    assert f"Deleted: {image_id_001}" in result
    assert f"Deleted: {image_id_002}" in result
