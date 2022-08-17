# Import comunity modules.

import os
import sys
import jinja2
import json

# Set module import path.

HERE = os.path.dirname(os.path.realpath(__file__))
APP_ROOT = os.path.join(HERE, "../", "../")
sys.path.insert(1, f"{APP_ROOT}")

from pkg.apt import apt
from pkg.http import http

template_loader = jinja2.FileSystemLoader(searchpath=f"{HERE}/template")
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template("terraform.dockerfile.j2")


def make_dockerfile(version) -> str:
    """Create docker file."""

    # Ensure dependencies
    dockerfile = apt.make_dockerfile("wget,unzip")

    if version == "latest":
        check_terraform_json = http.get(
            "https://checkpoint-api.hashicorp.com/v1/check/terraform"
        )
        check_terraform = json.loads(check_terraform_json)
        version = check_terraform["current_version"]

    dockerfile += template.render(version=version)
    return dockerfile
