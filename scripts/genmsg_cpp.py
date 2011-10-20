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

from __future__ import print_function

import os
import sys

import genmsg
from genmsg import log, plog, log_verbose
import genmsg.msgs 
import genmsg.gentools
import genmsg.command_line
import genmsg.base

try:
    from cStringIO import StringIO # Python 2.x
except ImportError:
    from io import StringIO # Python 3.x

MSG_TYPE_TO_CPP = {'byte': 'int8_t',
                   'char': 'uint8_t',
                   'bool': 'uint8_t',
                   'uint8': 'uint8_t',
                   'int8': 'int8_t', 
                   'uint16': 'uint16_t',
                   'int16': 'int16_t', 
                   'uint32': 'uint32_t',
                   'int32': 'int32_t',
                   'uint64': 'uint64_t',
                    'int64': 'int64_t',
                   'float32': 'float',
                   'float64': 'double',
                   'string': 'std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > ',
                   'time': 'ros::Time',
                   'duration': 'ros::Duration'}

def msg_type_to_cpp(type):
    """
    Converts a message type (e.g. uint32, std_msgs/String, etc.) into the C++ declaration
    for that type (e.g. uint32_t, std_msgs::String_<ContainerAllocator>)
    
    @param type: The message type
    @type type: str
    @return: The C++ declaration
    @rtype: str
    """
    (base_type, is_array, array_len) = genmsg.msgs.parse_type(type)
    cpp_type = None
    if (genmsg.msgs.is_builtin(base_type)):
        cpp_type = MSG_TYPE_TO_CPP[base_type]
    elif (len(base_type.split('/')) == 1):
        if (genmsg.msgs.is_header_type(base_type)):
            cpp_type = ' ::std_msgs::Header_<ContainerAllocator> '
        else:
            cpp_type = '%s_<ContainerAllocator> '%(base_type)
    else:
        pkg = base_type.split('/')[0]
        msg = base_type.split('/')[1]
        cpp_type = ' ::%s::%s_<ContainerAllocator> '%(pkg, msg)
        
    if (is_array):
        if (array_len is None):
            return 'std::vector<%s, typename ContainerAllocator::template rebind<%s>::other > '%(cpp_type, cpp_type)
        else:
            return 'boost::array<%s, %s> '%(cpp_type, array_len)
    else:
        return cpp_type

def cpp_message_declarations(name_prefix, msg):
    """
    Returns the different possible C++ declarations for a message given the message itself.
    
    @param name_prefix: The C++ prefix to be prepended to the name, e.g. "std_msgs::"
    @type name_prefix: str
    @param msg: The message type
    @type msg: str
    @return: A tuple of 3 different names.  cpp_message_decelarations("std_msgs::", "String") returns the tuple
        ("std_msgs::String_", "std_msgs::String_<ContainerAllocator>", "std_msgs::String")
    @rtype: str 
    """
    pkg, basetype = genmsg.names.package_resource_name(msg)
    cpp_name = ' ::%s%s'%(name_prefix, msg)
    if (pkg):
        cpp_name = ' ::%s::%s'%(pkg, basetype)
    return ('%s_'%(cpp_name), '%s_<ContainerAllocator> '%(cpp_name), '%s'%(cpp_name))

def escape_string(str):
    str = str.replace('\\', '\\\\')
    str = str.replace('"', '\\"')
    return str
        
def is_fixed_length(spec, includepath):
    """
    Returns whether or not the message is fixed-length
    
    @param spec: The message spec
    @type spec: genmsg.msgs.MsgSpec
    @param package: The package of the
    @type package: str
    """
    assert isinstance(includepath, list)
    types = []
    for field in spec.parsed_fields():
        if (field.is_array and field.array_len is None):
            return False
        
        if (field.base_type == 'string'):
            return False
        
        if (not field.is_builtin):
            types.append(field.base_type)
            
    types = set(types)
    for type in types:
        type = genmsg.msgs.resolve_type(type, spec.package)
        (_, new_spec) = genmsg.msg_loader.load_msg_by_type(msg_context, type, includepath, spec.package)
        if (not is_fixed_length(new_spec, includepath)):
            return False
        
    return True
    
def compute_full_text_escaped(gen_deps_dict):
    """
    Same as genmsg.gentools.compute_full_text, except that the
    resulting text is escaped to be safe for C++ double quotes

    @param get_deps_dict: dictionary returned by get_dependencies call
    @type  get_deps_dict: dict
    @return: concatenated text for msg/srv file and embedded msg/srv types. Text will be escaped for double quotes
    @rtype: str
    """
    definition = genmsg.gentools.compute_full_text(gen_deps_dict)
    lines = definition.split('\n')
    s = StringIO()
    for line in lines:
        line = escape_string(line)
        s.write('%s\\n\\\n'%(line))
        
    val = s.getvalue()
    s.close()
    return val

def default_value(type):
    """
    Returns the value to initialize a message member with.  0 for integer types, 0.0 for floating point, false for bool,
    empty string for everything else
    
    @param type: The type
    @type type: str
    """
    if type in ['byte', 'int8', 'int16', 'int32', 'int64',
                'char', 'uint8', 'uint16', 'uint32', 'uint64']:
        return '0'
    elif type in ['float32', 'float64']:
        return '0.0'
    elif type == 'bool':
        return 'false'

    return ""

def takes_allocator(type):
    """
    Returns whether or not a type can take an allocator in its constructor.  False for all builtin types except string.
    True for all others.
    
    @param type: The type
    @type: str
    """
    return not type in ['byte', 'int8', 'int16', 'int32', 'int64',
                        'char', 'uint8', 'uint16', 'uint32', 'uint64',
                        'float32', 'float64', 'bool', 'time', 'duration']

def generate_fixed_length_assigns(spec, container_gets_allocator, cpp_name_prefix):
    """
    Initialize any fixed-length arrays
    
    @param s: The stream to write to
    @type s: stream
    @param spec: The message spec
    @type spec: genmsg.msgs.MsgSpec
    @param container_gets_allocator: Whether or not a container type (whether it's another message, a vector, array or string)
        should have the allocator passed to its constructor.  Assumes the allocator is named _alloc.
    @type container_gets_allocator: bool
    @param cpp_name_prefix: The C++ prefix to use when referring to the message, e.g. "std_msgs::"
    @type cpp_name_prefix: str
    """
    # Assign all fixed-length arrays their default values
    for field in spec.parsed_fields():
        if (not field.is_array or field.array_len is None):
            continue

        val = default_value(field.base_type)
        if (container_gets_allocator and takes_allocator(field.base_type)):
            # String is a special case, as it is the only builtin type that takes an allocator
            if (field.base_type == "string"):
                string_cpp = msg_type_to_cpp("string")
                yield '    %s.assign(%s(_alloc));\n'%(field.name, string_cpp)
            else:
                (cpp_msg_unqualified, cpp_msg_with_alloc, _) = cpp_message_declarations(cpp_name_prefix, field.base_type)
                yield '    %s.assign(%s(_alloc));\n'%(field.name, cpp_msg_with_alloc)
        elif (len(val) > 0):
            yield '    %s.assign(%s);\n'%(field.name, val)


def generate_initializer_list(spec, container_gets_allocator):
    """
    Writes the initializer list for a constructor
    
    @param s: The stream to write to
    @type s: stream
    @param spec: The message spec
    @type spec: genmsg.msgs.MsgSpec
    @param container_gets_allocator: Whether or not a container type (whether it's another message, a vector, array or string)
        should have the allocator passed to its constructor.  Assumes the allocator is named _alloc.
    @type container_gets_allocator: bool
    """

    op = ':'
    for field in spec.parsed_fields():
        val = default_value(field.base_type)
        use_alloc = takes_allocator(field.base_type)
        if (field.is_array):
            if (field.array_len is None and container_gets_allocator):
                yield '  %s %s(_alloc)'%(op, field.name)
            else:
                yield '  %s %s()'%(op, field.name)
        else:
            if (container_gets_allocator and use_alloc):
                yield '  %s %s(_alloc)'%(op, field.name)
            else:
                yield '  %s %s(%s)'%(op, field.name, val)
        op = ','


def generator(spec, file_name, md5sum):

    yield '/* Auto-generated by genmsg_cpp for file %s */'%(file_name)
    yield '#ifndef %s_MESSAGE_%s_H'%(spec.package.upper(), spec.short_name.upper())
    yield '#define %s_MESSAGE_%s_H'%(spec.package.upper(), spec.short_name.upper())

    yield '#include <string>'
    yield '#include <vector>'
    yield ''
    yield '#include <ros/types.h>'
    yield '#include <ros/serialization.h>'
    yield '#include <ros/builtin_message_traits.h>'
    yield '#include <ros/message_operations.h>'
    yield ''
    
    # Includes for dependencies
    for field in spec.parsed_fields():
        if (not field.is_builtin):
            if (field.is_header):
                yield '#include <std_msgs/Header.h>'
            else:
                (package, name) = genmsg.names.package_resource_name(field.base_type)
                package = package or spec.package # convert '' to package
                yield '#include <%s/%s.h>'%(package, name)

    # namespace
    yield ''
    yield 'namespace %s'%(spec.package)
    yield '{'

    # struct
    yield 'template <class ContainerAllocator>'
    yield 'struct %s_ {\n'%(spec.short_name)
    yield '  typedef %s_<ContainerAllocator> Type;'%(spec.short_name)

    # constructors (with and without allocator)
    for (alloc_type,alloc_name) in [['',''],['const ContainerAllocator& ','_alloc']]:
        log('test')
        yield '  %s_(%s%s)'%(spec.short_name, alloc_type, alloc_name)

        # Write initializer list
        for l in generate_initializer_list(spec, alloc_name != '' ) :
            yield l
        
        yield '  {'

        # Fixed length arrays
        for l in generate_fixed_length_assigns(spec, alloc_name != '', '%s::'%(spec.package)):
            yield l

        yield '  }'
        yield ''

    # Members
    for field in spec.parsed_fields():
        cpp_type = msg_type_to_cpp(field.type)
        yield '  typedef %s _%s_type;'%(cpp_type, field.name)
        yield '  %s %s;'%(cpp_type, field.name)
        yield ''

    # Constants
    for constant in spec.constants:
        if (constant.type in ['byte', 'int8', 'int16', 'int32', 'int64', 'char', 'uint8', 'uint16', 'uint32', 'uint64']):
            yield '  enum { %s = %s };' % (constant.name, constant.val)
        else:
            yield '  static const %s %s;' % (msg_type_to_cpp(constant.type), constant.name)

    cpp_namespace = '::%s::'%(spec.package) # TODO handle nested namespace
    cpp_class = '%s_'%spec.short_name
    cpp_full_name = '%s%s'%(cpp_namespace,cpp_class)
    cpp_full_name_with_alloc = '%s<ContainerAllocator>'%(cpp_full_name)

    # Shared pointer typedefs
    yield ''
    yield '  typedef boost::shared_ptr< %s<ContainerAllocator> > Ptr;'%(cpp_full_name)
    yield '  typedef boost::shared_ptr< %s<ContainerAllocator> const> ConstPtr;'%(cpp_full_name)
    yield '  boost::shared_ptr<std::map<std::string, std::string> > __connection_header;'

    # End of struct
    yield ''
    yield '} // struct %s'%(cpp_class)

    # Typedef of template instance using std::allocator
    yield ''
    yield 'typedef %s<std::allocator<void> > %s;'%(cpp_full_name, spec.short_name)

    # Shared pointer typedefs
    yield ''
    yield 'typedef boost::shared_ptr< %s> MarkerPtr;'%(cpp_full_name)
    yield 'typedef boost::shared_ptr< %s const> MarkerConstPtr;'%(cpp_full_name)

    # Printer
    yield ''
    yield 'template<typename ContainerAllocator>'
    yield 'std::ostream& operator<<(std::ostream& s, const %s & v)'%(cpp_full_name_with_alloc)
    yield '{'
    yield 'ros::message_operations::Printer< %s >::stream(s, "", v);'%(cpp_full_name_with_alloc)
    yield 'return s;'
    yield '}'
    
    # End of namespace
    yield ''
    yield '} // namespace %s'%(spec.package)
   
    # Message Traits
    yield 'namespace ros'
    yield '{'
    yield 'namespace message_traits'
    yield '{'

    traits = ['IsMessage']
    if spec.has_header():
        traits.append('HasHeader')
    # TODO
    #if spec.is_fixed_length():
    #    traits = traits.append('IsFixedSize')

    # Binary traits
    for trait in traits:
        yield ''
        yield 'template<class ContainerAllocator> struct %s<%s > : public TrueType {};'%(trait, cpp_full_name_with_alloc)
        yield 'template<class ContainerAllocator> struct %s<%s const> : public TrueType {};'%(trait, cpp_full_name_with_alloc)

    # String traits
    for trait_class,trait_value in [['MD5Sum', md5sum], ['DataType', spec.full_name], ['Definition', 'todo']]: #TODO Definition
        yield ''
        yield 'template<class ContainerAllocator>'
        yield 'struct %s< %s > {'%(trait_class, cpp_full_name_with_alloc)
        yield '  static const char* value()'
        yield '  {'
        yield '    return "%s";'%(trait_value)
        yield '  }'
        yield ''
        yield '  static const char* value(const %s&) { return value(); }'%(cpp_full_name_with_alloc)
    
        if trait_class == 'MD5Sum':
            iter_count = len(trait_value) / 16
            for i in xrange(0, iter_count):
                start = i*16
                yield '  static const uint64_t static_value%s = 0x%sULL;'%((i+1), trait_value[start:start+16])
       
        yield '};'
    
    yield ''

    # End of traits
    yield '} // namespace message_traits'
    yield '} // namespace ros'
    yield ''

    # Serialization
    yield 'namespace ros'
    yield '{'
    yield 'namespace serialization'
    yield '{'
    yield ''

    yield 'template<class ContainerAllocator> struct Serializer< %s >'%(cpp_full_name_with_alloc)
    yield '{'

    yield '  template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)'
    yield '  {'

    for field in spec.parsed_fields():
        yield'    stream.next(m.%s);'%(field.name)
    
    yield '  }'
    yield ''

    yield '  ROS_DECLARE_ALLINONE_SERIALIZER;'

    yield '}; // struct %s'%(cpp_class)
    yield ''
    yield '} // namespace serialization'
    yield '} // namespace ros'


    # Message Operations

    yield ''
    yield 'namespace ros'
    yield '{'
    yield 'namespace message_operations'
    yield '{'
    yield ''

    # Printer operation

    yield 'template<class ContainerAllocator>'
    yield 'struct Printer<%s>'%(cpp_full_name_with_alloc)
    yield '{'
    yield '  template<typename Stream> static void stream(Stream& s, const std::string& indent, const %s& v)'%(cpp_full_name_with_alloc)
    yield '  {'

    for field in spec.parsed_fields():
        cpp_type = msg_type_to_cpp(field.base_type)
        if (field.is_array):
            yield '    s << indent << "%s[]" << std::endl;'%(field.name)
            yield '    for (size_t i = 0; i < v.%s.size(); ++i)'%(field.name)
            yield '    {'
            yield '      s << indent << "  %s[" << i << "]: ";'%(field.name)
            indent_increment = '  '
            if (not field.is_builtin):
                yield '      s << std::endl;'
                yield '      s << indent;'
                indent_increment = '    ';
            yield '      Printer<%s>::stream(s, indent + "%s", v.%s[i]);'%(cpp_type, indent_increment, field.name)
            yield '    }'
        else:
            yield '    s << indent << "%s: ";'%(field.name)
            indent_increment = '  '
            if (not field.is_builtin or field.is_array):
                yield '    s << std::endl;'
            yield '    Printer<%s>::stream(s, indent + "%s", v.%s);'%(cpp_type, indent_increment, field.name)

    yield '  }'
    yield '};'
    yield ''

    yield '} // namespace message_operations'
    yield '} // namespace ros'
    yield ''

    yield '#endif // %s_MESSAGE_%s_H'%(spec.package.upper(), spec.short_name.upper())
 
def print_sub_deps(msg_context, full_type_name, order):
    for dep_type_name in msg_context.get_depends(full_type_name):
        dep_file = msg_context.get_file(dep_type_name)
        print ("%s|-%s"%('  '*order,dep_type_name))
        print_sub_deps(msg_context, dep_type_name, order=1)
    return


def generate(args):
    """
    Generate a message
    
    @param msg_path: The path to the .msg file
    @type msg_path: str
    """

    from optparse import OptionParser
    parser = OptionParser("generates c++ message serialization code")

    parser.add_option('-p', dest='package', 
                      help="package name")
    parser.add_option('-v', dest='verbose', default=False, 
                      help="debug output", action='store_true')
    parser.add_option('-o', dest='outdir',
                      help="absolute path to output directory")
    parser.add_option('-I', dest='includepath', default=[],
                      help="include path to search for messages",
                      action='append')
    parser.add_option('-d', dest='deps', default=False,
                      help="list direct dependencies",
                      action="store_true")
    parser.add_option('-a', dest='all_deps', default=False,
                      help="list all dependencies",
                      action="store_true")
    (options, args) = parser.parse_args(args)

    log_verbose(options.verbose)

    # Read and parse the source msg file
    infile = os.path.abspath(args[1])
    msg_context = genmsg.msg_loader.MsgContext.create_default() # not used?
    full_type_name = genmsg.gentools.compute_full_type_name(options.package, os.path.basename(infile))
    spec = genmsg.msg_loader.load_msg_from_file(msg_context, infile, full_type_name)

    # Locate and parse dependencies
    search_path = genmsg.command_line.includepath_to_dict(options.includepath)
    try:
        genmsg.msg_loader.load_depends(msg_context, spec, search_path)
    except genmsg.InvalidMsgSpec as e:
        raise genmsg.MsgGenerationException("Cannot read .msg for %s: %s"%(full_type_name, str(e)))

    # Check if we should print the depencies
    if options.all_deps:
        print (full_type_name)
        print_sub_deps(msg_context, full_type_name, 0)
    elif options.deps:
        for dep_type_name in msg_context.get_depends(full_type_name):
            dep_file = msg_context.get_file(dep_type_name)
            print ("%s"%(dep_file))
        return

    # Create output directory
    try:
        os.makedirs(options.outdir)
    except OSError as e:
        if e.errno != 17: # file exists
            raise

    # Compute md5 sum of message
    md5sum = genmsg.compute_md5(msg_context, spec)

    # Write output file
    out_file_name = "%s.h"%spec.short_name
    out_file = os.path.join(options.outdir, out_file_name)
    with open(out_file, 'w') as f:
        for l in generator(spec, out_file_name, md5sum):
          f.write(l+'\n')

    return out_file

"""    
    s = StringIO()
    write_begin(s, spec, args[1])
    write_generic_includes(s)
    write_includes(s, spec)
    
    cpp_prefix = '%s::'%(options.package)
    
    s.write('namespace %s\n{\n'%(options.package))
    write_struct(s, spec, cpp_prefix, options.includepath)
    write_constant_definitions(s, spec)
    write_ostream_operator(s, spec, cpp_prefix)
    s.write('} // namespace %s\n\n'%(options.package))
    
    write_traits(s, spec, cpp_prefix, options.includepath)
    write_serialization(s, spec, cpp_prefix)
    write_operations(s, spec, cpp_prefix)


    if options.package == "std_msgs" and spec.short_name == "Header":
        s.write("#define STD_MSGS_INCLUDING_HEADER_DEPRECATED_DEF 1\n")
        s.write("#include <std_msgs/header_deprecated_def.h>\n")
        s.write("#undef STD_MSGS_INCLUDING_HEADER_DEPRECATED_DEF\n\n") 

    write_end(s, spec)
    
    if 'ROS_BUILD' in os.environ:
        package_dir = os.environ['ROS_BUILD']

    
    odir = os.path.join(options.outdir, options.package)

    if not os.path.exists(odir):
        # if we're being run concurrently, the above test can report false but os.makedirs can still fail if
        # another copy just created the directory
        try:
            os.makedirs(odir)
        except OSError as e:
            pass
         
    oname = '%s/%s.h' % (odir, spec.short_name)
    with open(oname, 'w') as f:
        print(f, s.getvalue(), file=f)
    
    s.close()
"""

if __name__ == "__main__":
    generate(sys.argv)
