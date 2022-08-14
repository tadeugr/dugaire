import os
import sys
import docker
from subprocess import run

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, f"{HERE}")

from pkg.my_util import my_util

_client = docker.from_env()


def get_image_short_id(image_id) -> str:
    """Get 12-character image id."""

    short_id = image_id.replace("sha256:", "")[:12]
    return short_id


def list_images():

    images = _client.images.list(
        filters={"label": my_util.get_dugaire_image_label()}, all=True
    )
    image_list = {}
    for image in images:
        short_id = get_image_short_id(image.id)
        image_list[short_id] = image
    return image_list


def get_children(image_short_id):

    cmd = f"docker images --filter since={image_short_id} -q"
    result = run(cmd, capture_output=True, shell=True)
    return result.stdout.splitlines()


def remove_image(image_id) -> bool:

    try:
        children = get_children(image_id)
        for child in children:
            remove_image(child)
        _client.images.remove(image=image_id, force=True)
        return True
    except docker.errors.ImageNotFound:
        return True
    except Exception:
        return False
