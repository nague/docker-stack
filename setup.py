#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from dockerstack.DockerStack import DockerStack

setup(
    name='dockerstack',
    version=DockerStack.VERSION,
    author = 'Lars Kellogg-Stedman',
    author_email = 'lars@oddbit.com',
    url = 'http://github.com/larsks/dockerize',
    packages=find_packages(),
    package_data={'dockerstack': ['templates/*']},
    entry_points={
        'console_scripts': [
            'stack = DockerStack.main:main'
        ]
    }
)