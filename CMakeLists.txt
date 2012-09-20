cmake_minimum_required(VERSION 2.8)
project(gencpp)
find_package(catkin REQUIRED COMPONENTS genmsg)

catkin_stack()
catkin_package(${PROJECT_NAME}
  CFG_EXTRAS gencpp-extras.cmake)

add_subdirectory(scripts)

file(WRITE ${CATKIN_BUILD_PREFIX}/${GENMSG_LANGS_DESTINATION}/gencpp "C++")
install(FILES ${CATKIN_BUILD_PREFIX}/${GENMSG_LANGS_DESTINATION}/gencpp
  DESTINATION ${GENMSG_LANGS_DESTINATION})

catkin_python_setup()
