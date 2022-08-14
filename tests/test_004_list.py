#!/usr/bin/env python3

# Import comunity modules.

import os
import sys
from click.testing import CliRunner

# Set module import path.

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, f"{HERE}/../dugaire")

# Import custom modules.

import dugaire
from pkg.my_app import my_app
import common

_BUILT_IMAGES = []


def test_list():
    """ "
    Run:
    dugaire build
    dugaire list
    """

    image_id = common.cli("build")
    assert 12 == len(image_id)

    result = common.cli(f"list")
    assert image_id in result


def test_list_not_short():
    """ "
    Run:
    dugaire build
    dugaire list --not-short
    """

    image_id = common.cli("build")
    assert 12 == len(image_id)

    result = common.cli(f"list --not-short")
    assert f"sha256:{image_id}" in result
