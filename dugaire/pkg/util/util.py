# Import comunity modules.

import os
import sys
import jinja2
import re

# Set module import path.

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, f"{HERE}")


def string_is_latest_or_version(check_string):
    prog = re.compile("^(\d+\.)?(\d+\.)?(\*|\d+)$")
    result = prog.match(check_string)

    if check_string != "latest" and not result:
        return False

    return True


def is_valid_version(version):
    """Check version format is valid."""

    prog = re.compile("^(\d+\.)?(\d+\.)?(\*|\d+)$")
    match_semantic_version = prog.match(version)

    if version != "latest" and not match_semantic_version:
        return False

    return True


def get_template(file_name, searchpath=f"{HERE}/templates"):
    """Load and return a Jinja template file."""

    templateLoader = jinja2.FileSystemLoader(searchpath=searchpath)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(file_name)
    return template


def get_dugaire_image_label(return_format="string"):
    """Get the default label used when building images."""

    default_label_key = "builtwith"
    default_label_value = "dugaire"
    default_label = {default_label_key: default_label_value}

    if return_format == "string":
        return f"{default_label_key}={default_label_value}"
    if return_format == "dockerfile":
        return f'{default_label_key}="{default_label_value}"'

    return default_label
