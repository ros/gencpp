install(
  FILES msg.h.template srv.h.template
  DESTINATION share/gencpp
  )

install(
  FILES gen_cpp.py
  DESTINATION share/gencpp/bin
  )