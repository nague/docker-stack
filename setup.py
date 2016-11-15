#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import codecs
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


install_requires = [
    'gitpython >= 2',
    'jinja2 >= 2',
    'docopt >= 0.6.1, < 0.7',
    'pyyaml >= 3.12',
    'validators',
    'requests',
    'clint',
    'PyYAML >= 3.08'
]

setup(
    name='docker-stack',
    version=find_version("dockerstack", "__init__.py"),
    description='This tool is used to generate easily and dynamically config files for docker.',
    author='DSanchez',
    author_email='dsanchez@kaliop.ca',
    url='',
    license='Apache License 2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points="""
    [console_scripts]
    docker-stack=dockerstack.main:main
    """,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
