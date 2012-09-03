install(
  FILES msg.h.template srv.h.template
  DESTINATION ${PROJECT_SHARE_DESTINATION})

install(
  FILES gen_cpp.py
  DESTINATION ${PROJECT_LIBEXEC_DESTINATION})
