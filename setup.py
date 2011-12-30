#!/usr/bin/env python

from setuptools import setup

# from gencpp import __version__

setup(name='gencpp',
#      version=__version__, FIXME
      version="0.0.0",
      packages=['gencpp'],
      package_dir={'':'src'},
      install_requires=['genmsg'],
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
