install(
  FILES msg.h.template srv.h.template
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

install(
  FILES gen_cpp.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
