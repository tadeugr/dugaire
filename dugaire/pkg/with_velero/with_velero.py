# Import comunity modules.

import os
import sys
import json
import jinja2
import urllib.request

# Set module import path.

HERE = os.path.dirname(os.path.realpath(__file__))
APP_ROOT = os.path.join(HERE, "../", "../")
sys.path.insert(1, f"{APP_ROOT}")

from pkg.apt import apt

template_loader = jinja2.FileSystemLoader(searchpath=f"{HERE}/template")
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template("velero.dockerfile.j2")


def make_dockerfile(version) -> str:

    # Ensure dependencies
    dockerfile = apt.make_dockerfile("wget")

    if version == "latest":
        response = urllib.request.urlopen(
            "https://api.github.com/repos/vmware-tanzu/velero/releases/latest"
        ).read()
        response = json.loads(response)
        version = response["tag_name"][1:]

    dockerfile += template.render(version=version)

    return dockerfile
