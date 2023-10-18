#! /usr/bin/env python

""" Gets the project version from the environment """

from os import environ
from setuptools import setup # type: ignore
from toml import load # type: ignore

if __name__ == '__main__':
    # Read pyproject.toml and extract the module name
    with open('pyproject.toml', 'r', encoding='utf-8') as f:
        config = load(f)
        module_name = config["project"]["name"]

    # Get the project version from the environment
    version = environ.get("TEAMHACK_VERSION")

    # Generate the version.py file
    with open(f'src/{module_name}/version.py', 'w', encoding='utf-8') as f:
        f.write(f'""" dynamically generated  """\n\n__version__ = "{version}"\n')

    setup(version=version)
