import os
from setuptools import find_packages, setup

# The directory containing this file
HERE = os.path.dirname(os.path.realpath(__file__))

# REAME content
README = open(os.path.join(HERE, "README.md")).read()

setup(
    name="dugaire",
    version="0.0.3",
    description="Build Docker images with custom packages for local development, testing and daily tasks.",
    long_description=README,
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
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=['certifi==2020.11.8', 'chardet==3.0.4', 'click==7.1.2', 'docker==4.3.1', 'idna==2.10', 'Jinja2==2.11.2', 'MarkupSafe==1.1.1', 'requests==2.25.0', 'six==1.15.0', 'urllib3==1.26.2', 'websocket-client==0.57.0'],
    entry_points={"console_scripts": ["dugaire=dugaire.dugaire:main"]},
)