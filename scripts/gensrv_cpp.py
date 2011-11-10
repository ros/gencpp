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

import genmsg_cpp
 
import sys
import os

import genmsg.srvs
import genmsg.gentools

def generate(srv_path, options):
    """
    Generate a service
    
    @param srv_path: the path to the .srv file
    @type srv_path: str
    """

    import em

    template_dir = (options.emdir)

    infile = os.path.abspath(srv_path)
    msg_context = genmsg.msg_loader.MsgContext.create_default()
    full_type_name = genmsg.gentools.compute_full_type_name(options.package, os.path.basename(infile))
    print(full_type_name, infile)
    spec = genmsg.msg_loader.load_srv_from_file(msg_context, infile, full_type_name)

    search_path = genmsg.command_line.includepath_to_dict(options.includepath)
    try:
        genmsg.msg_loader.load_depends(msg_context, spec, search_path)
    except genmsg.InvalidMsgSpec as e:
        raise genmsg.MsgGenerationException("Cannot read .msg for %s: %s"%(full_type_name, str(e)))

    out_file_name = os.path.join(options.outdir, spec.short_name + ".h")
    ofile = open(out_file_name, 'w')
    print (out_file_name)


    md5sum = genmsg.compute_md5(msg_context, spec)

    g={ "file_name_in":infile,
        "spec":spec,
        "md5sum":md5sum}

    interpreter = em.Interpreter(output=ofile, globals=g, options={"rawErrors_OPT":True})
    #interpreter.string(template_str)
    interpreter.file(open(template_dir+'/srv.h.template'))
    interpreter.shutdown()

    return

def generate_services(argv):
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
    generate_services(sys.argv)
    
