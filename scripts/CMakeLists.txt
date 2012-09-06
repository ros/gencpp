install(
  FILES msg.h.template srv.h.template
  DESTINATION ${CATKIN_PROJECT_SHARE_DESTINATION})

install(
  FILES gen_cpp.py
  DESTINATION ${CATKIN_PROJECT_BIN_DESTINATION})
