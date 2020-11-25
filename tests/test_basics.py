#!/usr/bin/env python3

""" Import comunity modules. """

import os
import sys
import pytest
from click.testing import CliRunner

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, f"{HERE}/../dugaire")

""" Import custom modules. """

import dugaire
import info

_BUILT_IMAGES = []


def test_help():

    cmd = ""
    cmd += "--help"

    result = CliRunner().invoke(dugaire.cli, cmd.split(" "))
    output = result.output.strip()

    assert f"Usage: cli [OPTIONS] COMMAND [ARGS]" in output


def test_version():

    cmd = ""
    cmd += "--version"

    result = CliRunner().invoke(dugaire.cli, cmd.split(" "))
    output = result.output.strip()

    info_version = info.get_version()
    info_prog_name = info.get_prog_name()

    assert f"{info_prog_name}, version {info_version}" == output


def test_build_default():
    global _BUILT_IMAGES

    cmd = ""
    cmd += "build"

    result = CliRunner().invoke(dugaire.cli, cmd.split(" "))
    output = result.output.strip()

    assert 12 == len(output)

    _BUILT_IMAGES.append(output)


def test_build_output_image_id():
    global _BUILT_IMAGES

    cmd = ""
    cmd += "build --output=image.id"

    result = CliRunner().invoke(dugaire.cli, cmd.split(" "))
    output = result.output.strip()

    assert 71 == len(output)

    _BUILT_IMAGES.append(output)


def test_build_output_image_name():
    global _BUILT_IMAGES

    cmd = ""
    cmd += "build --output=image.name"

    result = CliRunner().invoke(dugaire.cli, cmd.split(" "))
    output = result.output.strip()

    assert 21 == len(output)

    _BUILT_IMAGES.append(output)


def test_build_output_dockerfile():
    global _BUILT_IMAGES

    cmd = ""
    cmd += "build --output=dockerfile --dry-run"

    result = CliRunner().invoke(dugaire.cli, cmd.split(" "))
    output = result.output.strip()

    assert "LABEL builtwith" in output

def test_list_short():

    cmd = f"list --short"

    result = CliRunner().invoke(dugaire.cli, cmd.split(" "))
    output = result.output.strip()

    assert "Image ID:" in output
    assert "Image tags:" in output

def test_remove_image():
    global _BUILT_IMAGES

    cmd = ""
    cmd += f"remove --image={_BUILT_IMAGES[0]}"

    result = CliRunner().invoke(dugaire.cli, cmd.split(" "))
    output = result.output.strip()

    assert "Image removed." == output


def test_remove_all():
    global _BUILT_IMAGES

    cmd = ""
    cmd += f"remove --image=all"

    result = CliRunner().invoke(dugaire.cli, cmd.split(" "))
    output = result.output.strip()

    assert "Images removed." == output


def test_list_no_image():

    cmd = f"list"

    result = CliRunner().invoke(dugaire.cli, cmd.split(" "))
    output = result.output.strip()

    assert "No images built with dugaire found." == output
