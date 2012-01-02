cmake_minimum_required(VERSION 2.8)
project(gencpp)
find_package(catkin)

add_subdirectory(scripts)

catkin_project(gencpp
  VERSION 0.0.1
  CFG_EXTRAS gencpp-extras.cmake
  PYTHONPATH src
  )

file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/gencpp "C++")
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/gencpp
  DESTINATION etc/langs
  )

catkin_package(gencpp)
enable_python(gencpp)
