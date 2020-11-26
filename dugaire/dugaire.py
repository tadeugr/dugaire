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

import info
import util


@click.group()
@click.version_option(info.get_version(), prog_name=info.get_prog_name())
def cli():
    """ CLI tool to build and manage custom Docker images. """
    pass


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
    help="Comma separeted list of packages (no blank space) to install using apt-get install. Requires a base image with apt-get. Example: -apt=curl,vim",
    metavar="<pkg01|pkg01,pkg02>",
    required=False,
)
@click.option(
    "--pip3",
    help="Comma separeted list of packages (no blank space) to install using pip3 install. WARNING: requires -apt=python3-pip. Example: -apt=python3-pip -pip3=ansible,jinja2",
    metavar="<pkg01|pkg01,pkg02>",
    required=False,
)
@click.option(
    "--with-azurecli",
    "--with-az",
    help='Install Azure CLI. Examples: --with-azurecli=latest / For older versions, use pip3: --apt=python3-pip --pip="azure-cli==2.2.0"',
    metavar="<latest>",
    required=False,
    type=click.Choice(["latest"], case_sensitive=False),
)
@click.option(
    "--with-kubectl",
    help="Install kubectl. Examples: --with-kubectl=latest / --with-kubectl=1.17.0",
    metavar="<latest|1.15.0 (or other)>",
    required=False,
)
@click.option(
    "--with-velero",
    help="Install velero. Examples: --with-velero=latest / --with-velero=1.5.2",
    metavar="<latest|1.15.0 (or other)>",
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

    template = util.get_template("base.j2")
    dockerfile += template.render(
        from_=from_, label=util.get_dugaire_image_label("dockerfile")
    )

    if apt:
        packages = apt.replace(",", " ")
        template = util.get_template("apt.j2")
        dockerfile += template.render(packages=packages)

    if pip3:
        dependency_list = {}
        dependency_list["azure-cli"] = ["gcc", "python3-dev"]

        pip3_install = pip3.split(",")
        for package in pip3_install:
            package_name = package.split("==")[0]
            if package_name in dependency_list:
                dependency = " ".join(dependency_list[package_name])
                apt_template = util.get_template("apt.j2")
                dockerfile += apt_template.render(packages=dependency)

        packages = " ".join(pip3_install)
        template = util.get_template("pip3.j2")
        dockerfile += template.render(packages=packages)

    if with_kubectl:
        current_option_name = "--with-kubectl"
        current_option_value = with_kubectl

        if not util.string_is_latest_or_version(current_option_value):
            usage_msg = f"{current_option_name}=<latest | semantic versioning>"
            example_msg = f"{current_option_name}=latest | {current_option_name}=1.17.0"

            exc_msg = f"Bad usage {current_option_name}={current_option_value} \n"
            exc_msg += f"Valid usage: {usage_msg} \n"
            exc_msg += f"Examples: {example_msg}"
            raise click.BadOptionUsage(current_option_name, exc_msg)

        dependency_list = {}
        dependency_list = ["curl", "ca-certificates"]
        dependency = " ".join(dependency_list)

        apt_template = util.get_template("apt.j2")
        dockerfile += apt_template.render(packages=dependency)

        url = "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
        if with_kubectl != "latest":
            url = f"https://storage.googleapis.com/kubernetes-release/release/v{with_kubectl}/bin/linux/amd64/kubectl"

        template = util.get_template("with_kubectl.j2")
        dockerfile += template.render(url=url)

    if with_azurecli:
        dependency_list = {}
        dependency_list = ["curl", "ca-certificates"]
        dependency = " ".join(dependency_list)

        apt_template = util.get_template("apt.j2")
        dockerfile += apt_template.render(packages=dependency)

        template = util.get_template("with_azurecli.j2")
        dockerfile += template.render()

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

        if not with_kubectl:
            usage_msg = f"--with-kubectl=<latest | semantic versioning> {current_option_name}=<latest | semantic versioning>"
            example_msg = f"--with-kubectl=latest {current_option_name}=latest"

            exc_msg = f"Bad usage {current_option_name} requires --with-kubectl \n"
            exc_msg += f"Valid usage: {usage_msg} \n"
            exc_msg += f"Examples: {example_msg}"
            raise click.BadOptionUsage(current_option_name, exc_msg)

        dependency_list = {}
        dependency_list = ["wget"]
        dependency = " ".join(dependency_list)

        apt_template = util.get_template("apt.j2")
        dockerfile += apt_template.render(packages=dependency)

        if with_velero == "latest":
            import urllib.request

            response = urllib.request.urlopen(
                "https://api.github.com/repos/vmware-tanzu/velero/releases/latest"
            ).read()
            response = json.loads(response)
            with_velero = response["tag_name"][1:]

        template = util.get_template("with_velero.j2")
        dockerfile += template.render(version=with_velero)

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
    images = client.images.list(filters={"label": [util.get_dugaire_image_label()]})

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
@click.option(
    "--image",
    help="Comma separated list of Image IDs.",
    required=True,
    metavar="<Image ID|all>",
)
def remove(image):
    client = docker.from_env()

    if image == "all":
        images = client.images.list(filters={"label": [util.get_dugaire_image_label()]})
        for docker_image in images:
            client.images.remove(image=docker_image.id, force=True)

        click.echo("Images removed.")
        sys.exit(0)

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
