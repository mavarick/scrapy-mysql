#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
from pkgutil import walk_packages
from setuptools import setup


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
    url='https://github.com/mavarick/scrapy_mysql',
    packages=['scrapy_mysql'],
    package_dir={'': './'},
    install_requires=read_requirements('requirements-install.txt'),
    include_package_data=True,
    license="MIT",
    keywords='scrapy_mysql',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
