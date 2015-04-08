#!/usr/bin/env python
__copyright__ = 'Copyright 2015 LaunchKey, Inc.  See project license for usage.'
__author__ = 'Adam Englander (adam@launchkey.com)'

import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()

try:
    long_description = open('README.md', 'rt').read()
except IOError:
    long_description = ''

setup(
    name='launchkeywebdemo',
    version='1.0.0',

    description='LaunchKey Python SDK Web Example',
    long_description=long_description,

    author='LaunchKey',
    author_email='support@launchkey.com',

    url='https://launchkey.com',

    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        ],

    platforms=['Any'],

    scripts=[],
    provides=[],
    install_requires=[
        'launchkey-python==1.2.7', # LaunchKey SDK
        'pystache==0.5.4'          # Moustache templating
    ],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    data_files=[
        ('templates', ['templates/template.html'])
    ],

    entry_points={
        # This is the console script to be executed
        'console_scripts': [
            'launchkeywebdemo = webdemo.main:main'
        ],
    },

    zip_safe=False
)