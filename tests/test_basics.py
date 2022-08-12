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


def test_help():

    cmd = ""
    cmd += "--help"

    result = common.cli(cmd)

    assert f"Usage: cli [OPTIONS] COMMAND [ARGS]" in result


def test_version_parameter():
    """Test command: dugaire --version"""

    result = common.cli("--version")
    info_version = my_app.get_version()
    assert info_version == result


def test_version_command():
    """Test command: dugaire version"""

    result = common.cli("version")
    info_version = my_app.get_version()
    assert info_version == result


def test_build_default():
    global _BUILT_IMAGES

    cmd = ""
    cmd += "build"

    result = common.cli(cmd)

    assert 12 == len(result)

    _BUILT_IMAGES.append(result)

def test_build_random_name_output_image():
    global _BUILT_IMAGES

    cmd = ""
    cmd += "build --output=image.name"

    result = common.cli(cmd)

    assert 21 == len(result)

    _BUILT_IMAGES.append(result)

def test_build_name_output_image_id():
    global _BUILT_IMAGES

    cmd = ""
    cmd += "build --name=test_build_name_output_image_id --output=image.id"

    result = common.cli(cmd)

    assert 71 == len(result)

    _BUILT_IMAGES.append(result)


def test_build_output_dockerfile():
    global _BUILT_IMAGES

    cmd = ""
    cmd += "build --name=test_build_output_dockerfile --output=dockerfile --dry-run"

    result = common.cli(cmd)

    assert "LABEL builtwith" in result


def test_list_short():

    cmd = f"list --short"

    result = common.cli(cmd)

    assert "Image ID:" in result
    assert "Image tags:" in result


# def test_remove_image():
#     global _BUILT_IMAGES

#     cmd = ""
#     cmd += f"rmi {_BUILT_IMAGES[0]}"

#     result = common.cli(cmd)

#     assert f"Deleted: {_BUILT_IMAGES[0]}" in result


# def test_remove_all():
#     global _BUILT_IMAGES

#     cmd = ""
#     cmd += f"rmi all"

#     result = common.cli(cmd)

#     assert "Images removed." == result


# def test_list_no_image():

#     cmd = f"list"

#     result = common.cli(cmd)

#     assert "No images built with dugaire found." == result
