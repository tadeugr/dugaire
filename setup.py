import os
from setuptools import setup

_THIS_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

setup(
    name="tadeugr-dugaire",
    version="0.0.1",
    description="Quickly build docker images with custom packages",
    long_description=open(os.path.join(_THIS_SCRIPT_PATH, "README.md")).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tadeugr/dugaire",
    author="Tadeu Granemann",
    license='Apache License, Version 2.0',
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    #packages=["dugaire"],
    include_package_data=True,
    install_requires=["click", "docker", "jinja2"],
    entry_points={"console_scripts": ["dugaire=dugaire:main"]},
)