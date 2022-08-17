#!/usr/bin/env python3

# Import comunity modules.

import os
from platform import platform
import sys
import docker as docker_py
import click
import uuid
import click_completion
from io import BytesIO

# Set module import path.

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, f"{HERE}")

# Import custom modules.

from pkg.app import app
from pkg.cli import cli
from pkg.util import util
from pkg.docker import docker
from pkg.apt import apt
from pkg.pip3 import pip3
from pkg.with_kubectl import with_kubectl
from pkg.with_terraform import with_terraform
from pkg.with_velero import with_velero


@click.group()
@click.version_option(app.get_version(), message="%(version)s")
def cli_():
    """CLI tool to build and manage custom Docker images."""

    pass


@cli_.command()
def version():
    """Show the version and exit."""

    click.echo(app.get_version())


@cli_.command()
@click.option(
    "--from",
    "from_",
    help="Base image (used in Dockerfile FROM). Example: --from=ubuntu:20.04",
    metavar="<name:tag>",
    required=True,
    default="ubuntu:20.04",
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
    callback=cli.is_version_valid,
)
@click.option(
    "--with-terraform",
    "with_terraform_",
    help="Install terrafom. Examples: --with-terraform=latest / --with-terraform=0.15.5",
    metavar="<latest|semantic versioning>",
    required=False,
    callback=cli.is_version_valid,
)
@click.option(
    "--with-velero",
    "with_velero_",
    help="Install velero. Examples: --with-velero=latest / --with-velero=1.5.2",
    metavar="<latest|semantic versioning>",
    required=False,
    callback=cli.is_version_valid,
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
    with_terraform_,
    with_velero_,
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

    # Dockerfile: base image
    dockerfile += docker.make_dockerfile(from_)

    # Dockerfile: install packages using apt-get
    if apt_:
        dockerfile += apt.make_dockerfile(apt_)

    # Dockerfile: install packages using pip3
    if pip3_:
        # Ensure install python3-pip
        apt_python3_pip = "python3-pip"
        if not apt_ or apt_python3_pip not in apt_:
            dockerfile += apt.make_dockerfile(apt_python3_pip)

        dockerfile += pip3.make_dockerfile(pip3_)

    # Dockerfile: install kubectl
    if with_kubectl_:
        dockerfile += with_kubectl.make_dockerfile(with_kubectl_)

    # Dockerfile: install terraform
    if with_terraform_:
        dockerfile += with_terraform.make_dockerfile(with_terraform_)

    # Dockerfile: install velero
    if with_velero_:
        # Ensure kubectl
        if not with_kubectl_:
            dockerfile += with_kubectl.make_dockerfile("latest")

        dockerfile += with_velero.make_dockerfile(with_velero_)

    # Print dockerfile
    if output_ == "dockerfile":
        click.echo(dockerfile)

    image_id = None
    image_name = None
    if not dry_run:
        f = BytesIO(dockerfile.encode("utf-8"))
        client = docker_py.from_env()
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


@cli_.command("list", help="List images built with dugaire.")
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
    """
    List images built with dugaire.
    \n
    Examples:
    \n
    dugaire list
    \n
    dugaire list --no-short
    """

    client = docker_py.from_env()
    images = client.images.list(
        filters={"label": util.get_dugaire_image_label()}, all=True
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


@cli_.command()
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

    images_built_with_dugaire = docker.list_images()
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

        docker.remove_image(img_)
        click.echo(f"Deleted: {img_}")


def main():
    """Main function executed by the CLI command."""

    click_completion.init()
    cli_()


if __name__ == "__main__":
    """Call the main function."""

    main()
