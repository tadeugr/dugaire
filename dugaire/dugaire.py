import os
import sys
import docker
import fire
import jinja2
import yaml

_THIS_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, f"{_THIS_SCRIPT_PATH}/pkg")

from kubectl import kubectl

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

import fire

class Cli(object):

  install_list = []

  def install_order(self, pkg):
    if "depends_on" in pkg:
      for pkg in pkg["depends_on"]:
        self.install_order(pkg)
    
    self.install_list.append(pkg)
    


  def build(self):
    
    with open(f'{_THIS_SCRIPT_PATH}/pkg/config.yaml') as file:
      pkg_config = yaml.load(file, Loader=yaml.FullLoader)
      #print(pkg_config)

    for pkg in pkg_config["pkg"]:
      self.install_order(pkg)

    print(self.install_list)

    #outputText = kubectl.install()
    #print(outputText)

if __name__ == '__main__':
  fire.Fire(Cli)