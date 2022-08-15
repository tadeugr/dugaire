# Import comunity modules.

import os
import sys
import jinja2
import re

# Set module import path.

HERE = os.path.dirname(os.path.realpath(__file__))
APP_ROOT = os.path.join(HERE, "../", "../")
sys.path.insert(1, f"{APP_ROOT}")

from pkg.apt import apt
from pkg.http import http

template_loader = jinja2.FileSystemLoader(searchpath=f"{HERE}/template")
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template("kubectl.dockerfile.j2")


def make_dockerfile(version) -> str:
    # Ensure dependencies
    dockerfile = apt.make_dockerfile("curl,ca-certificates")

    if version == "latest":
        version = http.get(
            "https://dl.k8s.io/release/stable.txt"
        )

        version = version.replace("v", "")

    dockerfile += template.render(version=version)
    return dockerfile
