cmake_minimum_required(VERSION 2.8)
project(gencpp)
find_package(catkin)

add_subdirectory(scripts)

catkin_stack()
catkin_project(gencpp
  VERSION 0.0.1
  CFG_EXTRAS gencpp-extras.cmake
  )

file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/gencpp "C++")
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/gencpp
  DESTINATION etc/langs
  )

install(FILES stack.yaml
        DESTINATION share/gencpp)

catkin_export_python(src)
