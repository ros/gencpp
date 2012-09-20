#!/usr/bin/env python

from distutils.core import setup
from catkin.package import parse_package_for_distutils

d = parse_package_for_distutils()
d['packages'] = ['gencpp']
d['package_dir'] = {'': 'src'}
d['install_requires'] = ['genmsg']
d['scripts'] = ['scripts/gencpp.py']
setup(**d)
