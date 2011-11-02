if(gencpp_SOURCE_DIR)
  set(GENCPP_BIN ${gencpp_SOURCE_DIR}/scripts/genmsg_cpp.py CACHE FILEPATH "gencpp bin")
else()
  find_program(GENCPP_BIN genmsg_cpp.py)
endif()

if (NOT GENCPP_BIN)
  message(FATAL_ERROR "Unable to find gencpp binary genmsg_cpp.py")
endif()

message(STATUS "GENCPP_BIN found at ${GENCPP_BIN}")

macro(_generate_msgs_cpp ARG_PKG ARG_IFLAGS ARG_MSG_DEPS ARG_MESSAGES ARG_GEN_OUTPUT_DIR)

  set(ALL_GEN_OUTPUT_FILES_cpp "")
  foreach(msg ${ARG_MESSAGES})
    
    #Create input and output filenames
    get_filename_component(MSG_SHORT_NAME ${msg} NAME_WE)
    set(MSG_INPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/${msg})

    set(MSG_GENERATED_NAME ${MSG_SHORT_NAME}.h)
    set(GEN_OUTPUT_FILE ${ARG_GEN_OUTPUT_DIR}/${MSG_GENERATED_NAME})

    add_custom_command(OUTPUT ${GEN_OUTPUT_FILE}
      DEPENDS ${GENCPP_BIN} ${MSG_INPUT_FILE} ${ARG_MSG_DEPS}
      COMMAND 
      /usr/bin/env PYTHONPATH=${genmsg_PYTHONPATH}
      ${GENCPP_BIN} ${MSG_INPUT_FILE}
      -p ${ARG_PKG}
      -o ${ARG_GEN_OUTPUT_DIR}
      ${ARG_IFLAGS}
      COMMENT "Generating C++ code from ${ARG_PKG}/${MSG_SHORT_NAME}"
      )

    list(APPEND ALL_GEN_OUTPUT_FILES_cpp ${GEN_OUTPUT_FILE})
  endforeach()

endmacro()

macro(generate_msgs_cpp PKG)
  parse_arguments(PKG "MESSAGES;DEPENDENCIES" "" ${ARGN})
  
  message(">> generate_msg_cpp << PKG: ${PKG} MSGS: ${PKG_MESSAGES}  DEPNDS: ${PKG_DEPENDENCIES}")
  set(ALL_GEN_OUTPUT_FILES "")
  foreach(msg ${PKG_MESSAGES})
    
    #cpp specific
    # need: pkg_name, msg_short_name, Iflags, msg_deps, input file, output_dir
    set(MSG_GENERATED_NAME ${MSG_SHORT_NAME}.h)
    set(GEN_OUTPUT_FILE ${GEN_OUTPUT_DIR}/${MSG_GENERATED_NAME})
    message(STATUS "GenOutputFile=${GEN_OUTPUT_FILE}")

    add_custom_command(OUTPUT ${GEN_OUTPUT_FILE}
       DEPENDS ${GENCPP_BIN} ${MSG_INPUT_FILE} ${MSG_DEPS}
       COMMAND /usr/bin/env PYTHONPATH=${genmsg_PYTHONPATH}
       ${GENCPP_BIN} ${MSG_INPUT_FILE}
       -p ${PKG}
       -o ${GEN_OUTPUT_DIR}
       ${IFLAGS}
       COMMENT "Generating C++ code from ${PKG}/${MSG_SHORT_NAME}"
       )
     list(APPEND ALL_GEN_OUTPUT_FILES ${GEN_OUTPUT_FILE})

  endforeach() #msg
  message(STATUS "All Outputs: ${ALL_GEN_OUTPUT_FILES}")

  add_custom_target(${PKG}_gencpp ALL
    DEPENDS ${ALL_GEN_OUTPUT_FILES}
    )

  message(STATUS "DEP_TARGETS: ${DEP_TARGETS}")
  if(DEP_TARGETS)
    add_dependencies(${PKG}_gencpp ${DEP_TARGETS})
  endif(DEP_TARGETS)

endmacro()
