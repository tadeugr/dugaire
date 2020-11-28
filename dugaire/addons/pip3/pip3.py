import os
import sys
import click
import json
from typing import List

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, f"{HERE}")
sys.path.insert(1, f"{HERE}/../")

from common import module as common


class Pip3:
    def __init__(self, click_ctx=None):

        self.name = "pip3"
        self.option = f"--{self.name}"
        self.parameter = f"{self.name}"
        self.help_msg = f"Comma separeted list of packages (no blank space) to install using pip3 install. WARNING: requires --apt=python3-pip. Example: --apt=python3-pip {self.option}=ansible,jinja2"
        self.metavar = "<pkg01|pkg01,pkg02>"
        is_required = False

        if click_ctx:
            self.click_ctx = click_ctx
            self.option_value = self.click_ctx.params[self.parameter]

        self.dependencies = {}
        self.dependencies["__init__"] = {}
        self.dependencies["__init__"]["apt"] = ["python3-pip"]

        self.dependencies["azure-cli"] = {}
        self.dependencies["azure-cli"]["apt"] = ["gcc", "python3-dev"]

    def get_dockerfile(self, stack: List):

        option_value = self.option_value.split(",")
        option_value_no_version = []
        for value in option_value:
            option_value_no_version.append(value.split("==")[0])

        dependency_list = {}
        for requires in self.dependencies:
            is_init = requires == "__init__"
            is_in_stack = requires in stack
            is_in_option = requires in option_value_no_version

            if is_in_stack:
                continue
            if not is_init and not is_in_option:
                continue

            for manager in self.dependencies[requires]:
                for pkg in self.dependencies[requires][manager]:
                    if pkg in stack:
                        continue
                    else:
                        stack.append(pkg)
                    if manager not in dependency_list:
                        dependency_list[manager] = []
                    dependency_list[manager].append(pkg)

        dockerfile = ""
        for manager in dependency_list:
            packages = " ".join(dependency_list[manager])
            apt_template = common.util.get_template(
                f"{HERE}/../../templates", f"{manager}.j2"
            )
            dockerfile += apt_template.render(packages=packages)

        pip3_install = []
        for pkg in option_value:
            pkg_no_version = pkg.split("==")[0]
            if pkg_no_version in stack:
                continue
            pip3_install.append(pkg)
            stack.append(pkg_no_version)

        pip3_install = " ".join(pip3_install)
        template = common.util.get_template(HERE, f"{self.name}.j2")
        dockerfile += template.render(packages=pip3_install)

        return [dockerfile, stack]
