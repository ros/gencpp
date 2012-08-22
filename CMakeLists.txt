cmake_minimum_required(VERSION 2.8)
project(gencpp)
find_package(catkin REQUIRED)

add_subdirectory(scripts)

catkin_stack()
catkin_project(gencpp
  CFG_EXTRAS gencpp-extras.cmake
  )

file(WRITE ${catkin_BUILD_PREFIX}/etc/langs/gencpp "C++")
install(FILES ${catkin_BUILD_PREFIX}/etc/langs/gencpp
  DESTINATION etc/langs
  )

install(FILES stack.xml
        DESTINATION share/gencpp)

catkin_python_setup()
