cmake_minimum_required(VERSION 2.8)
project(gencpp)
find_package(catkin REQUIRED)

catkin_stack()
catkin_project(gencpp
  CFG_EXTRAS gencpp-extras.cmake
  )

add_subdirectory(scripts)

file(WRITE ${catkin_BUILD_PREFIX}/etc/langs/gencpp "C++")
install(FILES ${catkin_BUILD_PREFIX}/etc/langs/gencpp
  DESTINATION etc/langs
  )

catkin_python_setup()
