cmake_minimum_required(VERSION 2.8)
project(gencpp)
find_package(catkin)

add_subdirectory(scripts)

install_cmake_infrastructure(gencpp
  VERSION 0.0.1
  CFG_EXTRAS gencpp-extras.cmake
  PYTHONPATH src
  )

catkin_package(gencpp)