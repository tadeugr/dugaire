import os
import sys
import docker
#import fire
import click
import jinja2
import yaml
import urllib.request
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

  def install_curl(self, version = None):
    dockerfile = ''
    dockerfile += 'RUN apt-get install -qqy --no-install-recommends curl ca-certificates'
    dockerfile += "\n"
    return dockerfile

  def install_kubectl(self, version = None):

    download_url = 'https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl'
    if version and version != 'latest':
      download_url = f'https://storage.googleapis.com/kubernetes-release/release/v{version}/bin/linux/amd64/kubectl'

      try:
        if urllib.request.urlopen(download_url).getcode() != 200:
          raise Exception("URL error")
          
      except:
          print(f'Could not open URL {download_url}')
          sys.exit()


    dockerfile = ''
    dockerfile = self.install_curl()
    dockerfile += f'RUN curl -LO {download_url}'
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

      pkg_info = pkg.split(':')
      if len(pkg_info) > 2:
        print(f'{pkg} invalid format.')
        sys.exit()

      pkg_name = pkg_info[0]
      pkg_version = None
      if len(pkg_info) == 2:
        pkg_version = pkg_info[1]

      if not hasattr(self, 'install_'+pkg_name):
        print(f'{pkg} not supported.')
        sys.exit()

      dynamic_install = getattr(self, 'install_'+pkg_name)
      dockerfile += dynamic_install(pkg_version)

    print(dockerfile)

    #return True

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
    

@click.group()
def cli():
  pass

@cli.command()
@click.option('--from', '-f', 'from_', required=False)
@click.option('--install', '-i', multiple=True)
@click.option('--output', '-o', required=False)
def build(from_, install, output):
  #click.echo(install)
  dugaire = Dugaire()
  dugaire.build(install)
 
def main():
  cli()

if __name__ == '__main__':
  main()