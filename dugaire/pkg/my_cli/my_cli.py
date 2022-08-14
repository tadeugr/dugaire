import os
import re
import click
from rich import inspect

HERE = os.path.dirname(os.path.realpath(__file__))


def is_version_valid(ctx, param, value):
    if not value:
        return None

    if value == "latest":
        return value

    prog = re.compile("^(\d+\.)?(\d+\.)?(\*|\d+)$")
    match_semantic = prog.match(value)

    if not match_semantic:
        raise click.BadParameter(
            f'must be "latest" or semantic versioning (e.g 1.23.45).'
        )

    return value
