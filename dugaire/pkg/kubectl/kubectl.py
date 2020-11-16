import os
import jinja2

_THIS_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

def install():

    

    templateLoader = jinja2.FileSystemLoader(searchpath=_THIS_SCRIPT_PATH)
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "templates/install.j2"
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(version="1.13.0")

    return outputText