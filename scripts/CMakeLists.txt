cmake_minimum_required(VERSION 2.8)

install(
  PROGRAMS genmsg_cpp.py gensrv_cpp.py
  DESTINATION bin)

install(
  FILES msg.h.template srv.h.template
  DESTINATION share/gencpp
  )
