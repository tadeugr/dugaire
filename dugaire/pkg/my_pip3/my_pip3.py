import os
import jinja2

HERE = os.path.dirname(os.path.realpath(__file__))

template_loader = jinja2.FileSystemLoader(searchpath=f"{HERE}/template")
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template("pip3.dockerfile.j2")

def make_dockerfile(comma_separated_pkg_list) -> str:
  dockerfile = template.render(pip3_packages_list=comma_separated_pkg_list)
  return dockerfile