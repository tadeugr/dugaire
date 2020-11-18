import os
import sys
import docker
import click
import jinja2
import yaml
from io import BytesIO

_THIS_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, f"{_THIS_SCRIPT_PATH}/pkg")

@click.group()
def cli():
  pass

@cli.command()
#@click.option('--from', '-f', 'from_', required=False)
@click.option('--apt-install', '-apt', required=False)
@click.option('--with-kubectl', '-kubectl', required=False)
def build(apt_install, with_kubectl):

  dockerfile = ''
  dockerfile += 'FROM ubuntu:18.04'
  dockerfile += "\n"
  dockerfile += 'LABEL builtwith="dugaire"'
  dockerfile += "\n"
  dockerfile += 'RUN apt-get update -qq'
  dockerfile += "\n"
  dockerfile += f'RUN apt-get install -qqy --no-install-recommends curl ca-certificates'
  dockerfile += "\n"

  if apt_install:
    apt_install_pkgs = apt_install.replace(',', ' ')  
    dockerfile += f'RUN apt-get install -qqy --no-install-recommends {apt_install_pkgs}'
    dockerfile += "\n"

  if with_kubectl:
    download_url = 'https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl'
    if with_kubectl != 'latest':
      download_url = f'https://storage.googleapis.com/kubernetes-release/release/v{version}/bin/linux/amd64/kubectl'

    dockerfile += f'RUN curl -LO {download_url}'
    dockerfile += "\n"
    dockerfile += 'RUN chmod +x ./kubectl'
    dockerfile += "\n"
    dockerfile += 'RUN mv ./kubectl /usr/local/bin'
    dockerfile += "\n"
  
  print('********')
  print(dockerfile)
  print('********')

  f = BytesIO(dockerfile.encode('utf-8'))
  client = docker.from_env()
  image, _ = client.images.build(
      fileobj=f,
      #path='.',
      #dockerfile='Dockerfile',
      tag='customimage',
      #buildargs='version=1.13.0'
  )
  print(image)
  print(_)
  object_methods = [method_name for method_name in dir(image)
                if callable(getattr(image, method_name))]
  #print(object_methods)
  #print(image.__dict__)

  print(image.attrs["Id"])
  print(image.attrs["RepoTags"])

@cli.command('list')
def list_():
  print('list')

def main():
  cli()

if __name__ == '__main__':
  main()