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

    def __init__(self, click_ctx=None):

        self.name = "apt"
        self.option = f"--with-{self.name}"
        self.parameter = f"with_{self.name}"
        
        if click_ctx:
            self.click_ctx = click_ctx
            self.option_value = self.click_ctx.params[self.parameter]

        self.dependencies = {"apt": ["wget"]}

    def get_dockerfile(self, stack):

        option_value = self.option_value.split(",")
        apt_install = []
        for pkg in option_value:
            if pkg in stack:
                continue
            apt_install.append(pkg)
            stack.append(apt_install)
        
        packages = " ".join(apt_install)
        template = common.util.get_template(HERE, f"{self.name}.j2")
        dockerfile += template.render(packages=packages)
        return [dockerfile, stack]
