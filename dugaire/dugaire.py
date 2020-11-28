#!/usr/bin/env python3

""" Import comunity modules. """

import os
import sys
import docker
import click
import jinja2
import json
import uuid
import re
import click_completion
import urllib.request
from io import BytesIO

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, f"{HERE}")

""" Import custom modules. """

from common import module as common
from addons import module as addons


@click.group()
@click.pass_context
@click.version_option(common.info.get_version(), prog_name=common.info.get_prog_name())
def cli(ctx):
    """ CLI tool to build and manage custom Docker images. """
    pass


@cli.command()
@click.pass_context
@click.option(
    "--from",
    "from_",
    help="Base image (used in Dockerfile FROM). Example: --from=ubuntu:20.04",
    metavar="<name:tag>",
    required=True,
    default="ubuntu:18.04",
    show_default=True,
    type=str,
)
@click.option(
    "--name",
    help='Image name. Example: --name="myimage:0.0.1"',
    metavar="<name:tag>",
    required=False,
    default="random",
    show_default=True,
)
@click.option(
    "--apt",
    help="Comma separeted list of packages (no blank space) to install using apt-get install. Requires a base image with apt-get. Example: --apt=curl,vim",
    metavar="<pkg01|pkg01,pkg02>",
    required=False,
)
@click.option(
    "--pip3",
    help="Comma separeted list of packages (no blank space) to install using pip3 install. Example: --pip3=ansible,jinja2==2.11.2",
    metavar="<pkg01|pkg01,pkg02>",
    required=False,
)
@click.option(
    "--with-azurecli",
    help='Install Azure CLI. Examples: --with-azurecli=latest / For older versions, use pip3: --pip3="azure-cli==2.2.0"',
    metavar="latest",
    required=False,
    type=click.Choice(["latest"], case_sensitive=False),
)
@click.option(
    "--with-kubectl",
    help="Install kubectl. Examples: --with-kubectl=latest / --with-kubectl=1.17.0",
    metavar="<latest|semantic versioning>",
    required=False,
)
@click.option(
    "--with-velero",
    help="Install velero. Examples: --with-velero=latest / --with-velero=1.5.2",
    metavar="<latest|semantic versioning>",
    required=False,
)
@click.option(
    "--force",
    help="Ignore Docker cache and build from scratch.",
    required=False,
    default=False,
    show_default=True,
    is_flag=True,
)
@click.option(
    "--dry-run",
    help="Do not build image.",
    required=False,
    default=False,
    show_default=True,
    is_flag=True,
)
@click.option(
    "--output",
    help="Command output options.",
    required=False,
    default="image.id.short",
    show_default=True,
    type=click.Choice(
        ["image.id", "image.id.short", "image.name", "dockerfile"], case_sensitive=False
    ),
)
def build(
    ctx,
    from_,
    name,
    apt,
    pip3,
    with_azurecli,
    with_kubectl,
    with_velero,
    force,
    dry_run,
    output,
):
    """
    Build Docker images with custom packages.
    \n
    Examples:
    \n
    Build an image and install vim and curl using apt-get.
    \n
    $ dugaire build --apt=vim,curl
    \n
    Build an image and install python3 using apt-get and ansible using pip3.
    \n
    $ dugaire build --apt=python3-pip --pip3=ansible
    \n
    Build an image and install the latest version of kubectl.
    \n
    $ dugaire build --with-kubectl=latest
    \n

    """

    dockerfile = ""
    stack = []

    template = common.util.get_template(f"{HERE}/templates", "base.j2")
    dockerfile += template.render(
        from_=from_, label=common.util.get_dugaire_image_label("dockerfile")
    )

    if apt:
        addon = addons.apt.Apt(ctx)
        addon_dockerfile, stack = addon.get_dockerfile(stack)
        dockerfile += addon_dockerfile

    if pip3:
        addon = addons.pip3.Pip3(ctx)
        addon_dockerfile, stack = addon.get_dockerfile(stack)
        dockerfile += addon_dockerfile

    if with_kubectl:
        addon = addons.kubectl.Kubectl(ctx)
        is_success, msg = addon.validate_option()
        if not is_success:
            raise click.BadOptionUsage(addon.option, msg)
        addon_dockerfile, stack = addon.get_dockerfile(stack)
        dockerfile += addon_dockerfile

    if with_azurecli:
        azurecli = addons.azurecli.Azurecli(ctx)
        azurecli_dockerfile, stack = azurecli.get_dockerfile(stack)
        dockerfile += azurecli_dockerfile

    if with_velero:
        velero = addons.velero.Velero(ctx)
        is_success, msg = velero.validate_option()
        if not is_success:
            raise click.BadOptionUsage(velero.option, msg)
        velero_dockerfile, stack = velero.get_dockerfile(stack)
        dockerfile += velero_dockerfile

    """Build image."""

    image_id = None
    image_name = None
    if not dry_run:
        f = BytesIO(dockerfile.encode("utf-8"))
        client = docker.from_env()
        image_name = name
        if image_name == "random":
            random_name = str(uuid.uuid4())[:8]
            random_tag = str(uuid.uuid4())[:8]
            image_name = f"dug-{random_name}:{random_tag}"

        image, error = client.images.build(
            fileobj=f, tag=image_name, nocache=force, rm=True, forcerm=True
        )

        image_id = image.attrs["Id"]
        image_name = image.attrs["RepoTags"][0]

    if output == "image.id":
        click.echo(image_id)
    if output == "image.id.short":
        click.echo(image_id.replace("sha256:", "")[:12])
    if output == "image.name":
        click.echo(image_name)
    if output == "dockerfile":
        click.echo(dockerfile)


@cli.command("list", help="List images built with dugaire.")
@click.option(
    "--short/--not-short",
    "-s",
    help="Print short or full image ID.",
    required=False,
    default=True,
    show_default=True,
    is_flag=True,
)
def list_(short):
    client = docker.from_env()
    images = client.images.list(
        filters={"label": [common.util.get_dugaire_image_label()]}
    )

    if not len(images):
        click.echo("No images built with dugaire found.")
        sys.exit(0)

    for image in images:
        image_id = image.id
        if short:
            image_id = image_id.replace("sha256:", "")[:12]

        click.echo(f"-----------")
        click.echo(f"Image ID: {image_id}")
        join_image_tags = " ".join(image.tags)
        click.echo(f"Image tags: {join_image_tags}")
    click.echo(f"-----------")


@cli.command(help="Remove images built with dugaire.")
@click.pass_context
@click.option(
    "--image",
    help="Comma separated list of Image IDs.",
    required=True,
    metavar="<Image ID|all>",
)
def remove(ctx, image):
    client = docker.from_env()

    if image == "all":
        images = client.images.list(
            filters={"label": [common.util.get_dugaire_image_label()]}
        )
        for docker_image in images:
            client.images.remove(image=docker_image.id, force=True)

        click.echo("Images removed.")
        ctx.exit(0)

    client.images.remove(image=image, force=True)
    click.echo("Image removed.")


def patch_click() -> None:
    """Fix Click ASCII encoding issue."""
    try:
        from click import core
        from click import _unicodefun  # type: ignore
    except ModuleNotFoundError:
        return

    for module in (core, _unicodefun):
        if hasattr(module, "_verify_python3_env"):
            module._verify_python3_env = lambda: None


def main():
    """Main function executed by the CLI command."""
    patch_click()
    click_completion.init()
    cli()


if __name__ == "__main__":
    """Call the main function."""
    main()
