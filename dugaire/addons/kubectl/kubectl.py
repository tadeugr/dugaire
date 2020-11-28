import os
import sys
import click
import json
from typing import List

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, f"{HERE}")
sys.path.insert(1, f"{HERE}/../")

from common import module as common


class Kubectl:
    def __init__(self, click_ctx=None):

        self.name = "kubectl"
        self.option = f"--with-{self.name}"
        self.parameter = f"with_{self.name}"
        self.examples_msg = f"Examples: {self.option}=latest / {self.option}=1.17.0"
        self.help_msg = f"Install kubectl. {self.examples_msg}"
        self.metavar = "<latest|semantic versioning>"
        is_required = False

        if click_ctx:
            self.click_ctx = click_ctx
            self.option_value = self.click_ctx.params[self.parameter]

        self.dependencies = {"apt": ["curl", "ca-certificates"]}

    def validate_option(self):

        if not common.util.is_latest_or_version(self.option_value):
            error_msg = f"Bad usage {self.option}={self.option_value} \n"
            error_msg += f"To get help, run: dugaire build --help"
            return [False, error_msg]

        return [True, None]

    def get_dockerfile(self, stack: List):

        dependency_list = {}
        for manager in self.dependencies:
            for pkg in self.dependencies[manager]:
                if pkg in stack:
                    continue
                else:
                    stack.append(pkg)
                if manager not in dependency_list:
                    dependency_list[manager] = []
                dependency_list[manager].append(pkg)
        stack.append(self.name)

        dockerfile = ""
        for manager in dependency_list:
            packages = " ".join(dependency_list[manager])
            apt_template = common.util.get_template(
                f"{HERE}/../../templates", f"{manager}.j2"
            )
            dockerfile += apt_template.render(packages=packages)

        url = "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
        if self.option_value != "latest":
            url = f"https://storage.googleapis.com/kubernetes-release/release/v{self.option_value}/bin/linux/amd64/kubectl"

        template = common.util.get_template(HERE, f"{self.name}.j2")
        dockerfile += template.render(url=url)

        return [dockerfile, stack]
