#!/usr/bin/env python3

""" Import comunity modules. """

from gc import callbacks
import os
from platform import platform
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
from rich import inspect

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, f"{HERE}")

""" Import custom modules. """

from pkg.my_app import my_app
from pkg.my_cli import my_cli
from pkg.my_util import my_util
from pkg.my_docker import my_docker
from pkg.my_apt import my_apt
from pkg.my_pip3 import my_pip3
from pkg.with_kubectl import with_kubectl

import util


@click.group()
@click.version_option(my_app.get_version(), message="%(version)s")
def cli():
    """CLI tool to build and manage custom Docker images."""
    pass


@cli.command()
def version():
    """Show the version and exit."""

    click.echo(my_app.get_version())


@cli.command()
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
    "apt_",
    help="Comma separeted list of packages (no blank space) to install using apt-get install. Requires a base image with apt-get. Example: -apt=curl,vim",
    metavar="<pkg01|pkg01,pkg02>",
    required=False,
)
@click.option(
    "--pip3",
    "pip3_",
    help="Comma separeted list of packages (no blank space) to install using pip3 install. WARNING: requires -apt=python3-pip. Example: -apt=python3-pip -pip3=ansible,jinja2",
    metavar="<pkg01|pkg01,pkg02>",
    required=False,
)
@click.option(
    "--with-kubectl",
    "with_kubectl_",
    help="Install kubectl. Examples: --with-kubectl=latest / --with-kubectl=1.17.0",
    metavar="<latest|semantic versioning>",
    required=False,
    callback=my_cli.is_version_valid
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
    "-o",
    "output_",
    help="Command output options.",
    required=False,
    default="image.id.short",
    show_default=True,
    type=click.Choice(
        ["image.id", "image.id.short", "image.name", "dockerfile"], case_sensitive=False
    ),
)
def build(
    from_,
    name,
    apt_,
    pip3_,
    with_kubectl_,
    with_velero,
    force,
    dry_run,
    output_,
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

    template = util.get_template("base.j2")    
    dockerfile += template.render(
        from_=from_, label=util.get_dugaire_image_label("dockerfile")
    )

    if apt_:
        dockerfile += my_apt.make_dockerfile(apt_)

    if pip3_:
        # Ensure install python3-pip
        apt_python3_pip = "python3-pip"
        if not apt_ or apt_python3_pip not in apt_:
            dockerfile += my_apt.make_dockerfile(apt_python3_pip)

        dockerfile += my_pip3.make_dockerfile(pip3_)

    if with_kubectl_:
        dockerfile += with_kubectl.make_dockerfile(with_kubectl_)

    if with_velero:

        current_option_name = "--with-velero"
        current_option_value = with_velero

        if not util.string_is_latest_or_version(current_option_value):
            usage_msg = f"{current_option_name}=<latest | semantic versioning>"
            example_msg = f"{current_option_name}=latest | {current_option_name}=1.5.2"

            exc_msg = f"Bad usage {current_option_name}={current_option_value} \n"
            exc_msg += f"Valid usage: {usage_msg} \n"
            exc_msg += f"Examples: {example_msg}"
            raise click.BadOptionUsage(current_option_name, exc_msg)

        if not with_kubectl_:
            usage_msg = f"--with-kubectl=<latest | semantic versioning> {current_option_name}=<latest | semantic versioning>"
            example_msg = f"--with-kubectl=latest {current_option_name}=latest"

            exc_msg = f"Bad usage {current_option_name} requires --with-kubectl \n"
            exc_msg += f"Valid usage: {usage_msg} \n"
            exc_msg += f"Examples: {example_msg}"
            raise click.BadOptionUsage(current_option_name, exc_msg)

        dockerfile += my_apt.make_dockerfile("wget")

        if with_velero == "latest":
            import urllib.request

            response = urllib.request.urlopen(
                "https://api.github.com/repos/vmware-tanzu/velero/releases/latest"
            ).read()
            response = json.loads(response)
            with_velero = response["tag_name"][1:]

        template = util.get_template("with_velero.j2")
        dockerfile += template.render(version=with_velero)

    if output_ == "dockerfile":
        click.echo(dockerfile)

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

        # --platform linux/amd64
        image, error = client.images.build(
            fileobj=f, tag=image_name, nocache=force, rm=True, forcerm=True
        )

        image_id = image.attrs["Id"]
        image_name = image.attrs["RepoTags"][0]

    if output_ == "image.id":
        click.echo(image_id)
    if output_ == "image.id.short":
        click.echo(image_id.replace("sha256:", "")[:12])
    if output_ == "image.name":
        click.echo(image_name)


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
    images = client.images.list(filters = { "label" : util.get_dugaire_image_label()}, all=True)

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


@cli.command()
@click.argument(
    "image_",
    required=True,
    nargs=-1,
    metavar="image",
)
def rmi(image_):
    """
    Remove images built with dugaire.
    \n
    Examples:
    \n
    Remove all images.
    \n
    $ dugaire rmi all
    \n
    Remove an image by image ID.
    \n
    $ dugaire rmi 205f13fdada0
    \n
    Remove multiple images by image ID.
    \n
    $ dugaire rmi 205f13fdada0 758581506147
    \n

    """

    client = docker.from_env()

    # built_images = client.images.list(filters={"label": [util.get_dugaire_image_label()]})
    images_built_with_dugaire = my_docker.list_images()
    if len(images_built_with_dugaire) == 0:
        click.echo("No images built with dugaire found.")
        exit(0)

    if "all" in image_:
        image_ = images_built_with_dugaire

    # Iterate image ID arguments
    for img_ in image_:
        if img_ not in images_built_with_dugaire.keys() and img_ != "all":
            click.echo(f"{img_} was not built with dugaire. Skipping...")
            continue

        my_docker.remove_image(img_)
        click.echo(f"Deleted: {img_}")

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

    # It seems newer click version does not require patching
    # patch_click()
    click_completion.init()
    cli()


if __name__ == "__main__":
    """Call the main function."""

    main()
