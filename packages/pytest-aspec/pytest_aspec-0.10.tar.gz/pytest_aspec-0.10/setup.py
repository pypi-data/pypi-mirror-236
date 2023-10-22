#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup


def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    with open(path) as f:
        return f.read()


setup(
    name='pytest_aspec',
    version='0.10',
    description='A rspec format reporter for pytest',
    long_description=read('README.rst'),
    author='2ps',
    author_email='p.shingavi@yahoo.com',
    url='https://github.com/angry-penguins/pytest-aspec',
    keywords='pytest pspec test report bdd rspec',
    install_requires=[
        'pytest>=3.0.0',
        'six>=1.11.0',
    ],
    scripts=['bin/pspec'],
    packages=['pytest_aspec'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'pspec = pytest_aspec.plugin',
        ],
    },
)
