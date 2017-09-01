#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
from pkgutil import walk_packages
from setuptools import setup, find_packages


def read_file(filename):
    with io.open(filename) as fp:
        return fp.read().strip()


def read_rst(filename):
    # Ignore unsupported directives by pypi.
    content = read_file(filename)
    return ''.join(line for line in io.StringIO(content)
                   if not line.startswith('.. comment::'))


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name='scrapy_mysql',
    version=read_file('VERSION'),
    description="mysql based components for Scrapy.",
    long_description=read_rst('README.md'),
    author="Mavarick",
    author_email='mavarick.liu@yahoo.com',
    url='https://github.com/mavarick/scrapy-mysql',
    packages=['scrapy_mysql'],
    package_dir={'': '.'},
    install_requires=read_requirements('requirements-install.txt'),
    include_package_data=True,
    license="MIT",
    keywords='scrapy_mysql',
)
