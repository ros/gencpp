cmake_minimum_required(VERSION 2.8)
find_package(ros_cmake)
#find_package(genmsg)

add_subdirectory(scripts)

install_cmake_infrastructure(gencpp
  VERSION 1.3.1 
  CFG_EXTRAS gencpp-extras.cmake
  )
