#!/usr/bin/env python3

import os
import sys
import docker
import click
import jinja2
import uuid
from io import BytesIO

_THIS_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, f"{_THIS_SCRIPT_PATH}/pkg")

def get_template(file_name):
  templateLoader = jinja2.FileSystemLoader(searchpath=f"{_THIS_SCRIPT_PATH}/templates")
  templateEnv = jinja2.Environment(loader=templateLoader)
  TEMPLATE_FILE = file_name
  template = templateEnv.get_template(TEMPLATE_FILE)
  return template

@click.group()
def cli():
  pass

@cli.command()
@click.option('--apt-install', '-apt', 
  help='Comma separeted list of packages (no blank space). Example: -apt=curl,vim',
  required=False
)
@click.option('--pip3-install', '-pip3',
  help='Comma separeted list of packages (no blank space). Example: -pip3=ansible,jinja2',
  required=False
)
@click.option('--with-kubectl',
  help="Install kubectl version. Examples: --with-kubectl=latest / --with-kubectl=1.17.0",
  required=False
)
@click.option('--name', '-n',
  help='Image name.',
  required=False,
  default='random',
  show_default=True
)
@click.option('--dry-run',
  help='Do not build image.',
  required=False,
  default=False,
  show_default=True,
  is_flag=True
)
@click.option('--output', '-o',
  help='Command output options.',
  required=False,
  default='image-id',
  show_default=True,
  type=click.Choice(['image-id', 'image-name', 'dockerfile'], case_sensitive=False)
)
def build(apt_install, pip3_install, with_kubectl, name, dry_run, output):
  """
  Build Docker images with custom packages.
  \n
  Examples:
  \n
  Build an image and install vim and curl using apt-get.
  \n
  $ dugaire build -apt=vim,curl
  \n
  Build an image and install python3 using apt-get and ansible using pip3.
  \n
  $ dugaire build -apt=python3-pip -pip3=ansible
  \n
  Build an image and install the latest version of kubectl.
  \n
  $ dugaire build --with-kubectl=latest
  \n

  """

  dockerfile = ''

  template = get_template('base.j2')
  dockerfile += template.render()

  if apt_install:
    packages = apt_install.replace(',', ' ')
    template = get_template('apt_install.j2')
    dockerfile += template.render(packages=packages)

  if pip3_install:
    packages = pip3_install.replace(',', ' ')
    template = get_template('pip3_install.j2')
    dockerfile += template.render(packages=packages)

  if with_kubectl:
    url = 'https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl'
    if with_kubectl != 'latest':
      url = f'https://storage.googleapis.com/kubernetes-release/release/v{with_kubectl}/bin/linux/amd64/kubectl'

    template = get_template('with_kubectl.j2')
    dockerfile += template.render(url=url)
  
  #print(dockerfile)
  #sys.exit()

  image_id = None
  image_name = None
  if not dry_run:
    f = BytesIO(dockerfile.encode('utf-8'))
    client = docker.from_env()
    image_name = name
    if image_name == 'random':
      random_uuid = str(uuid.uuid4())
      image_name = f'dug-{random_uuid}'
      
    image, error = client.images.build(
        fileobj=f,
        tag=image_name,
    )
    
    image_id = image.attrs["Id"]
    image_name = image.attrs["RepoTags"]
  
  if output == 'image-id':
    click.echo(image_id)
  if output == 'image-name':
    click.echo(image_name)
  if output == 'dockerfile':
    click.echo(dockerfile)
  

def main():
  cli()

if __name__ == '__main__':
  main()