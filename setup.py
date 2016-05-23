#!/usr/bin/env python

"""
Stock alarm program
"""

from setuptools import setup
from setuptools import find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='stock-alarm',
    version='0.1',
    description='Get email notifications for your stock portfolio',
    long_description=long_description,
    url='https://github.com/fuuccker/stock-alarm',
    author='Facundo Ferrin',
    author_email='facundo.ferrin@gmail.com',
    license='MIT',
    keywords='stock market stockholders',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers, Stockholders',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=['beautifulsoup4 > 4'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'console_scripts': [
    #         'stock-alarm=stock-alarm:main',
    #     ],
    # },
)