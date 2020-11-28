#!/usr/bin/env python3

""" Import comunity modules. """

import os
import sys
import docker
import click
import jinja2
import json
import uuid
import re
import click_completion
import urllib.request
import subprocess
from io import BytesIO

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, f"{HERE}")

""" Import custom modules. """

sys.path.insert(1, f"{HERE}/../dugaire")
from common import module as common


def make():
    template = common.util.get_template(f"{HERE}/..", f"README.j2")

    result = subprocess.run(["dugaire", "build", "--help"], stdout=subprocess.PIPE)
    usage_help = result.stdout.decode("utf8")

    rendered = template.render(usage_help=usage_help)
    print(rendered)
    return rendered


make()
