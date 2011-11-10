Source: @(CATKIN_PACKAGE_PREFIX)gencpp
Section: misc
Priority: extra
Maintainer: Troy Straszheim <straszheim@willowgarage.com>
Build-Depends: debhelper (>= 7), cmake, make, catkin
Homepage: <insert the upstream URL, if relevant>

Package: @(CATKIN_PACKAGE_PREFIX)gencpp
Architecture: all
Depends: ${misc:Depends} @(CATKIN_PACKAGE_PREFIX)genmsg
Description: It generates cpp, it does
 <insert long description, indented with spaces>
X-ROS-Pkg-Name: gencpp
X-ROS-Pkg-Depends: catkin, genmsg
X-ROS-System-Depends:
