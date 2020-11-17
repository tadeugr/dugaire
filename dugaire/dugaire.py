import os
import sys
import docker
#import fire
import click
import jinja2
import yaml
from io import BytesIO

_THIS_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, f"{_THIS_SCRIPT_PATH}/pkg")

#from kubectl import kubectl

#client = docker.from_env()
#client.containers.run("ubuntu:18.04", "echo hello world")
# image, _ = client.images.build(
#     path='.',
#     dockerfile='Dockerfile',
#     tag='customimage',
#     #buildargs='version=1.13.0'
# )
# print(image)
# print(_)



class Dugaire():

  def install_curl(self):
    dockerfile = ''
    dockerfile += 'RUN apt-get install -qqy --no-install-recommends curl ca-certificates'
    dockerfile += "\n"
    return dockerfile

  def install_kubectl(self):
    dockerfile = ''
    dockerfile = self.install_curl()
    dockerfile += 'RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl'
    dockerfile += "\n"
    dockerfile += 'RUN chmod +x ./kubectl'
    dockerfile += "\n"
    dockerfile += 'RUN mv ./kubectl /usr/local/bin'
    dockerfile += "\n"
    return dockerfile

  def build(self, install):
    dockerfile = ''
    dockerfile += 'FROM ubuntu:18.04'
    dockerfile += "\n"
    dockerfile += 'LABEL builtwith="dugaire"'
    dockerfile += "\n"
    dockerfile += 'RUN apt-get update -qq'
    dockerfile += "\n"

    for pkg in install:
      #click.echo(pkg)
      dynamic_install = getattr(self, 'install_'+pkg)
      dockerfile += dynamic_install()

    print(dockerfile)

    return True

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

@click.group()
def cli():
  pass

@cli.command()
@click.option('--from', '-f', 'from_', required=False)
@click.option('--install', '-i', multiple=True)
@click.option('--output', '-o', required=False)
def build(from_, install, output):
  click.echo(install)
  dugaire = Dugaire()
  dugaire.build(install)
 
def main():
  cli()

if __name__ == '__main__':
  main()