import os
from setuptools import find_packages, setup

# The directory containing this file
HERE = os.path.dirname(os.path.realpath(__file__))

# REAME content
README = open(os.path.join(HERE, "README.md")).read()

setup(
    name="dugaire",
    version="0.0.1",
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
    install_requires=["click", "docker", "jinja2"],
    entry_points={"console_scripts": ["dugaire=dugaire.dugaire:main"]},
)