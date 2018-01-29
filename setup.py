# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='pyliwc',
    version='0.1.0',
    description='LIWC',
    long_description=readme,
    author='Daniel Federschmidt',
    author_email='daniel@federschmidt.xyz',
    url='https://github.com/dfederschmidt/pyliwc',
    packages=find_packages(exclude=('tests', 'docs'))
)