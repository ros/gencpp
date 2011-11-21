#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2009, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

## ROS message source code generation for C++
## 
## Converts ROS .msg files in a package into C++ source code implementations.

import sys
import os
import em

import genmsg.gentools
import genmsg.command_line

msg_template_map = { 'msg.h.template':'@NAME@.h' }
srv_template_map = { 'srv.h.template':'@NAME@.h' }

def generate_from_templates(input_file, msg_context, spec, output_dir, template_dir, template_map):

    md5sum = genmsg.compute_md5(msg_context, spec)

    g = { "file_name_in":input_file,
          "spec":spec,
          "md5sum":md5sum}

    for template_file_name, output_file_name in template_map.items():
        template_file = os.path.join(template_dir, template_file_name)
        output_file = os.path.join(output_dir, output_file_name.replace("@NAME@", spec.short_name))

        #print "generate_from_template %s %s %s" % (input_file, template_file, output_file) 

        ofile = open(output_file, 'w') #todo try
        
        # todo, reuse interpreter
        interpreter = em.Interpreter(output=ofile, globals=g, options={em.RAW_OPT:True,em.BUFFERED_OPT:True})
        if not os.path.isfile(template_file):
            raise RuntimeError, "Template file %s not found in template dir %s" % (template_file_name, template_dir)
        interpreter.file(open(template_file)) #todo try
        interpreter.shutdown()


def generate(input_file, options):
    """
    Generate a service
    
    @param srv_path: the path to the .srv file
    @type srv_path: str
    """
    try:
        os.makedirs(options.outdir)
    except OSError as e:
        if e.errno != 17: # file exists
            raise


    input_file = os.path.abspath(input_file)
    msg_context = genmsg.msg_loader.MsgContext.create_default()
    full_type_name = genmsg.gentools.compute_full_type_name(options.package, os.path.basename(input_file))

    if( options.includepath ):
        search_path = genmsg.command_line.includepath_to_dict(options.includepath)
    else:
        search_path = {}


    if input_file.endswith(".msg"):
        spec = genmsg.msg_loader.load_msg_from_file(msg_context, input_file, full_type_name)
    elif input_file.endswith(".srv"):
        spec = genmsg.msg_loader.load_srv_from_file(msg_context, input_file, full_type_name)        
    else:
        assert False, "Uknown file extension for %s"%input_file

    try:
        genmsg.msg_loader.load_depends(msg_context, spec, search_path)
    except genmsg.InvalidMsgSpec as e:
        raise genmsg.MsgGenerationException("Cannot read .msg for %s: %s"%(full_type_name, str(e)))

    if input_file.endswith(".msg"):
        generate_from_templates(input_file,
                                msg_context,
                                spec,
                                options.outdir,
                                options.emdir,
                                msg_template_map)
    elif input_file.endswith(".srv"):
        generate_from_templates(input_file,
                                msg_context,
                                spec,
                                options.outdir,
                                options.emdir,
                                srv_template_map)
        generate_from_templates(input_file,
                                msg_context,
                                spec.request,
                                options.outdir,
                                options.emdir,
                                msg_template_map)
        generate_from_templates(input_file,
                                msg_context,
                                spec.response,
                                options.outdir,
                                options.emdir,
                                msg_template_map)

def generate_cl(argv):
    # print argv
    from optparse import OptionParser
    parser = OptionParser("gencpp_srv.py [options] <srv file>")
    parser.add_option("-p", dest='package',
                      help="package name")
    parser.add_option("-o", dest='outdir',
                      help="directory in which to place output files")
    parser.add_option("-I", dest='includepath',
                      help="include path to search for messages",
                      action="append")
    parser.add_option("-e", dest='emdir',
                      help="directory containing empy templates",
                      default=sys.path[0])

    (options, argv) = parser.parse_args(argv)

    if( not options.package or not options.outdir or len(argv) != 2):
        parser.print_help()
        exit(-1)

    generate(argv[1], options)

if __name__ == "__main__":
    generate_cl(sys.argv)
    
