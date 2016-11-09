#!/usr/bin/env python

import sys

from setuptools import setup, find_packages

if not sys.version_info[0] == 3:
    print('only python3 supported!')
    sys.exit(1)

setup(name='coastSHARK',
      version='1.0.0',
      description='Collect AST Information for smartSHARK.',
      install_requires=['javalang', 'mongoengine', 'pymongo'],
      author='atrautsch',
      author_email='alexander.trautsch@stud.uni-goettingen.de',
      url='https://gitlab.drecks-provider.de/werkzeuge/kyk',
      download_url='https://gitlab.drecks-provider.de/werkzeuge/kyk/repository/archive.tar.gz?ref=release',
      test_suite='coastSHARK.tests',
      packages=find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache2.0 License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
     )