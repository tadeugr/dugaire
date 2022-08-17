#!/usr/bin/env python3

# Import comunity modules

import os
import sys
import jinja2
import subprocess

# Set module import path.

HERE = os.path.dirname(os.path.realpath(__file__))
APP_ROOT = os.path.join(HERE, "../", "../")
sys.path.insert(0, HERE)
sys.path.insert(1, APP_ROOT)

# Global vars

template_loader = jinja2.FileSystemLoader(searchpath=f"{HERE}/template")
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template("README.md.j2")


def make():

    result = subprocess.run(["dugaire", "--help"], stdout=subprocess.PIPE)
    usage_help = result.stdout.decode("utf8")

    result = subprocess.run(["dugaire", "build", "--help"], stdout=subprocess.PIPE)
    usage_build_help = result.stdout.decode("utf8")

    rendered = template.render(usage_help=usage_help, usage_build_help=usage_build_help)
    print(rendered)
    return rendered


make()
