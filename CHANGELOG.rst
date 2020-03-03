^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package gencpp
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.6.5 (2020-03-03)
------------------
* add operator== & operator!= to message generation (`#41 <https://github.com/ros/gencpp/issues/41>`_)

0.6.4 (2020-03-02)
------------------
* [windows] reducing the odds to have name collisions (`#47 <https://github.com/ros/gencpp/issues/47>`_)

0.6.3 (2020-01-24)
------------------
* various code cleanup (`#46 <https://github.com/ros/gencpp/issues/46>`_)
* package.xml format 3 (`#45 <https://github.com/ros/gencpp/issues/45>`_)
* use setuptools instead of distutils (`#43 <https://github.com/ros/gencpp/issues/43>`_)
* bump CMake version to avoid CMP0048 warning (`#44 <https://github.com/ros/gencpp/issues/44>`_)
* two patches to make the generated headers reproducible (`#42 <https://github.com/ros/gencpp/issues/42>`_)

0.6.2 (2019-03-18)
------------------
* add plugins the ability to also generate free functions (`#40 <https://github.com/ros/gencpp/issues/40>`_)

0.6.1 (2019-03-04)
------------------
* enable Windows build (`#38 <https://github.com/ros/gencpp/issues/38>`_)

0.6.0 (2018-01-29)
------------------
* add plugin support for generated C++ message headers (`#32 <https://github.com/ros/gencpp/pull/32>`_)
* put all the message integer constants into a common enum (`#25 <https://github.com/ros/gencpp/issues/25>`_)

0.5.5 (2016-06-27)
------------------
* fix extra semicolon warning (`#26 <https://github.com/ros/gencpp/issues/26>`_)

0.5.4 (2016-03-14)
------------------
* fix unused parameter warning (`#24 <https://github.com/ros/gencpp/issues/24>`_)

0.5.3 (2014-12-22)
------------------
* remove copyright header from generated code (`#20 <https://github.com/ros/gencpp/issues/20>`_)

0.5.2 (2014-05-07)
------------------
* add architecture_independent flag in package.xml (`#19 <https://github.com/ros/gencpp/issues/19>`_)

0.5.1 (2014-02-24)
------------------
* use catkin_install_python() to install Python scripts (`#18 <https://github.com/ros/gencpp/issues/18>`_)
* add 'u' suffix to unsigned enum values to avoid compiler warning (`#16 <https://github.com/ros/gencpp/issues/16>`_)

0.5.0 (2014-01-29)
------------------
* remove __connection_header from message template (`#3 <https://github.com/ros/gencpp/issues/3>`_)

0.4.16 (2014-01-27)
-------------------
* fix warning about empty message definition (`ros/ros_comm#344 <https://github.com/ros/ros_comm/issues/344>`_)

0.4.15 (2014-01-07)
-------------------
* python 3 compatibility
* fix generated code of message definition with windows line endings (`#6 <https://github.com/ros/gencpp/issues/6>`_)

0.4.14 (2013-08-21)
-------------------
* make gencpp relocatable (`ros/catkin#490 <https://github.com/ros/catkin/issues/490>`_)

0.4.13 (2013-06-18)
-------------------
* update message targets to depend on template
* update msg template to generate empty functions without warnings about unused variables (`#4 <https://github.com/ros/gencpp/issues/4>`_)

0.4.12 (2013-03-08)
-------------------
* fix handling spaces in folder names (`ros/catkin#375 <https://github.com/ros/catkin/issues/375>`_)

0.4.11 (2012-12-21)
-------------------
* first public release for Groovy
