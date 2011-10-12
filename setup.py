#!/usr/bin/env python

from setuptools import setup

setup(name='gencpp',
      version= '0.1.0',
      packages=[],
      package_dir = {'':'src'},
      install_requires=['genmsg'],
      scripts = ['scripts/genmsg_cpp.py', 'scripts/gensrv_cpp.py'],
      author = "Josh Faust, Troy Straszheim", 
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
