import os
import sys
import click
import json
from typing import List

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, f"{HERE}")
sys.path.insert(1, f"{HERE}/../")

from common import module as common


class Apt:

    name: str
    option: str
    option_value: str
    parameter: str
    help_msg: str
    metavar: str
    is_required: bool
    click_ctx: None
    dependencies: List
    pkgs: List

    def __init__(self, click_ctx=None):

        self.name = "apt"
        self.option = f"--with-{self.name}"
        self.parameter = f"with_{self.name}"
        self.help_msg = (
            f"Install apt. Examples: {self.option}=latest / {self.option}=1.5.2"
        )
        self.metavar = "<latest|semantic versioning>"
        is_required = False

        if click_ctx:
            self.click_ctx = click_ctx
            self.option_value = self.click_ctx.params[self.parameter]

        self.dependencies = {"apt": ["wget"]}

    def get_click_option(self):

        option = click.Option(
            [self.option],
            help=self.help_msg,
            metavar=self.metavar,
            required=False,
        )

        return option

    def validate_option(self):

        if not common.util.is_latest_or_version(self.option_value):
            usage_msg = f"{self.option}=<latest | semantic versioning>"
            example_msg = f"{self.option}=latest | {self.option}=1.5.2"

            error_msg = f"Bad usage {self.option}={self.option_value} \n"
            error_msg += f"Valid usage: {usage_msg} \n"
            error_msg += f"Examples: {example_msg}"
            return {"is_success": False, "msg": error_msg}

        if not self.click_ctx.params["with_kubectl"]:
            error_msg = f"{self.option} requires --with-kubectl"
            return {"is_success": False, "msg": error_msg}

        return {"is_success": True, "msg": None}

    def get_dockerfile(self, stack=None):
        dependency_list = []
        for dependency in self.dependencies["apt"]:
            if dependency in stack:
                continue
            dependency_list.append(dependency)

        packages = " ".join(dependency_list)
        dockerfile = ""
        apt_template = common.util.get_template(f"{HERE}/../../templates", "apt.j2")
        dockerfile += apt_template.render(packages=packages)

        if self.option_value == "latest":
            import urllib.request

            response = urllib.request.urlopen(
                "https://api.github.com/repos/vmware-tanzu/apt/releases/latest"
            ).read()
            response = json.loads(response)
            with_apt = response["tag_name"][1:]

        template = common.util.get_template(HERE, f"{self.parameter}.j2")
        dockerfile += template.render(version=with_apt)
        return dockerfile
