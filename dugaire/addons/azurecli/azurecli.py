import os
import sys
import click
import json
from typing import List

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, f"{HERE}")
sys.path.insert(1, f"{HERE}/../")

from common import module as common


class Azurecli:

    def __init__(self, click_ctx=None):

        self.name = "azurecli"
        self.option = f"--with-{self.name}"
        self.parameter = f"with_{self.name}"
        self.help_msg = (
            f'Install Azure CLI. Examples: {self.option}=latest / For older versions, use pip3: --apt=python3-pip --pip="azure-cli==2.2.0"'
        )
        is_required = False

        self.choices = ['latest']

        if click_ctx:
            self.click_ctx = click_ctx
            self.option_value = self.click_ctx.params[self.parameter]

        self.dependencies = {"apt": ["curl", "ca-certificates"]}

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

        template = common.util.get_template(HERE, f"{self.name}.j2")
        dockerfile += template.render()
        return [dockerfile, stack]
