#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from dockerstack.DockerStack import DockerStack


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='dockerstack',
    description='This tool is used to generate easily and dynamically config files for docker.',
    long_description=readme(),
    version=DockerStack.VERSION,
    author='DSanchez',
    author_email='dsanchez@kaliop.ca',
    url='',
    license='MIT',
    packages=find_packages(),
    package_data={'dockerstack': ['templates/*']},
    entry_points={
        'console_scripts': [
            'stack = DockerStack.main:main'
        ]
    },
    install_requires=[
        'gitpython',
        'jinja2'
    ]
)
