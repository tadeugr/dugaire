#!/usr/bin/env python3

""" Import comunity modules. """

import os
import sys
from click.testing import CliRunner

HERE = os.path.dirname(os.path.realpath(__file__))


""" Import custom modules. """

sys.path.insert(0, f"{HERE}")
import helper

sys.path.insert(1, f"{HERE}/../dugaire")
import dugaire
import info

_BUILT_IMAGES = []


def test_help():

    cmd = ""
    cmd += "--help"

    result = helper.cli(cmd)

    assert f"Usage: cli [OPTIONS] COMMAND [ARGS]" in result


def test_version():

    cmd = ""
    cmd += "--version"

    result = helper.cli(cmd)

    info_version = info.get_version()
    info_prog_name = info.get_prog_name()

    assert f"{info_prog_name}, version {info_version}" == result


def test_build_default():
    global _BUILT_IMAGES

    cmd = ""
    cmd += "build"

    result = helper.cli(cmd)

    assert 12 == len(result)

    _BUILT_IMAGES.append(result)


def test_build_output_image_id():
    global _BUILT_IMAGES

    cmd = ""
    cmd += "build --output=image.id"

    result = helper.cli(cmd)

    assert 71 == len(result)

    _BUILT_IMAGES.append(result)


def test_build_output_image_name():
    global _BUILT_IMAGES

    cmd = ""
    cmd += "build --output=image.name"

    result = helper.cli(cmd)

    assert 21 == len(result)

    _BUILT_IMAGES.append(result)


def test_build_output_dockerfile():
    global _BUILT_IMAGES

    cmd = ""
    cmd += "build --output=dockerfile --dry-run"

    result = helper.cli(cmd)

    assert "LABEL builtwith" in result


def test_list_short():

    cmd = f"list --short"

    result = helper.cli(cmd)

    assert "Image ID:" in result
    assert "Image tags:" in result


def test_remove_image():
    global _BUILT_IMAGES

    cmd = ""
    cmd += f"remove --image={_BUILT_IMAGES[0]}"

    result = helper.cli(cmd)

    assert "Image removed." == result


def test_remove_all():
    global _BUILT_IMAGES

    cmd = ""
    cmd += f"remove --image=all"

    result = helper.cli(cmd)

    assert "Images removed." == result


def test_list_no_image():

    cmd = f"list"

    result = helper.cli(cmd)

    assert "No images built with dugaire found." == result
