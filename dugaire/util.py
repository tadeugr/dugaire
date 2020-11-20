#!/usr/bin/env python3

""" Import comunity modules. """

import os
import sys
import jinja2

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, f"{HERE}")


def get_template(file_name):
    """ Load and return a Jinja template file. """

    templateLoader = jinja2.FileSystemLoader(searchpath=f"{HERE}/templates")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = file_name
    template = templateEnv.get_template(TEMPLATE_FILE)
    return template


def get_dugaire_image_label(return_format="string"):
    """ Get the default label used when building images. """

    default_label_key = "builtwith"
    default_label_value = "dugaire"
    default_label = {default_label_key: default_label_value}

    if return_format == "string":
        return f"{default_label_key}={default_label_value}"
    if return_format == "dockerfile":
        return f'{default_label_key}="{default_label_value}"'

    return default_label
