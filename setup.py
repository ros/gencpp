#!/usr/bin/env python

from __future__ import print_function
from setuptools import setup
import sys
from xml.etree.ElementTree import ElementTree

try:
    root = ElementTree(None, 'stack.xml')
    version = root.findtext('version')
except Exception as e:
    print('Could not extract version from your stack.xml:\n%s' % e, file=sys.stderr)
    sys.exit(1)

setup(name = 'gencpp',
      version = version,
      packages = ['gencpp'],
      package_dir = {'': 'src'},
      install_requires = ['genmsg'],
      scripts = ['scripts/gen_cpp.py'],
      author = "Morgen Kjaergaard, Troy Straszheim, Josh Faust",
      author_email = "straszheim@willowgarage.com",
      url = "http://www.ros.org/wiki/gencpp",
      download_url = "http://pr.willowgarage.com/downloads/gencpp/",
      keywords = ["ROS"],
      classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License" ],
      description = "ROS msg/srv C++ generation",
      long_description = """\
Library and scripts for generating ROS message data structures in C++.
""",
      license = "BSD"
      )
