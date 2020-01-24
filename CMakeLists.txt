cmake_minimum_required(VERSION 3.0.2)
project(gencpp)
find_package(catkin REQUIRED COMPONENTS genmsg)

catkin_package(
  CATKIN_DEPENDS genmsg
  CFG_EXTRAS gencpp-extras.cmake
)

add_subdirectory(scripts)

file(WRITE ${CATKIN_DEVEL_PREFIX}/${GENMSG_LANGS_DESTINATION}/gencpp "C++")
install(FILES ${CATKIN_DEVEL_PREFIX}/${GENMSG_LANGS_DESTINATION}/gencpp
  DESTINATION ${GENMSG_LANGS_DESTINATION})

catkin_python_setup()
