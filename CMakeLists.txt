cmake_minimum_required(VERSION 3.8)
project(witmotion_ros)

# Add support for C++17
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Subdirectories
add_subdirectory(witmotion-uart-qt)

# Directories
include_directories(include)
include_directories(witmotion-uart-qt/include)

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_srvs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(rosgraph_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(Qt5 COMPONENTS SerialPort REQUIRED)
find_package(rcl_interfaces REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(lifecycle_msgs REQUIRED)

# MOC for Qt
set(CMAKE_AUTOMOC ON)
qt5_wrap_cpp(MOC_SOURCES include/witmotion_ros.h)

add_library(witmotion_ros
    ${MOC_SOURCES}
    src/witmotion_ros.cpp
)

# Consolidate includes and libraries
set(INCLUDE_DIRS 
    ${ament_cmake_INCLUDE_DIRS}
    ${tf2_INCLUDE_DIRS}
    ${tf2_geometry_msgs_INCLUDE_DIRS}
    ${rclcpp_INCLUDE_DIRS}
    ${std_srvs_INCLUDE_DIRS}
    ${sensor_msgs_INCLUDE_DIRS}
    ${geometry_msgs_INCLUDE_DIRS}
    ${nav_msgs_INCLUDE_DIRS}
    ${rosgraph_msgs_INCLUDE_DIRS}
    ${std_msgs_INCLUDE_DIRS}
    ${Qt5Core_INCLUDE_DIRS}
    ${Qt5SerialPort_INCLUDE_DIRS}
    ${rcl_interfaces_INCLUDE_DIRS}
    ${rclcpp_lifecycle_INCLUDE_DIRS}
    ${lifecycle_msgs_INCLUDE_DIRS}
)
include_directories(${INCLUDE_DIRS})

set(LIBS 
    ${ament_cmake_LIBRARIES}
    ${tf2_LIBRARIES}
    ${tf2_geometry_msgs_LIBRARIES}
    ${rclcpp_LIBRARIES}
    ${std_srvs_LIBRARIES}
    ${sensor_msgs_LIBRARIES}
    ${geometry_msgs_LIBRARIES}
    ${nav_msgs_LIBRARIES}
    ${rosgraph_msgs_LIBRARIES}
    ${std_msgs_LIBRARIES}
    ${Qt5Core_LIBRARIES}
    ${Qt5SerialPort_LIBRARIES}
    ${rcl_interfaces_LIBRARIES}
    ${rclcpp_lifecycle_LIBRARIES}
    ${lifecycle_msgs_LIBRARIES}
)

target_link_libraries(witmotion_ros ${LIBS} witmotion-uart Qt5::Core Qt5::SerialPort)

# Exports and installations
ament_export_dependencies(
    ament_cmake
    tf2
    tf2_geometry_msgs
    rclcpp
    std_srvs
    sensor_msgs
    geometry_msgs
    nav_msgs
    rosgraph_msgs
    std_msgs
    witmotion_ros
    witmotion-uart
    Qt5Core
    Qt5SerialPort
)
ament_export_include_directories(${INCLUDE_DIRS})
ament_export_libraries(witmotion_ros witmotion-uart)

install(
    TARGETS witmotion-uart
    EXPORT export_witmotion-uart
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION lib
)

install(
    TARGETS witmotion_ros
    EXPORT export_witmotion_ros
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION lib
)

add_executable(witmotion_ros_node src/witmotion_ros_node.cpp)
target_link_libraries(witmotion_ros_node witmotion_ros)
ament_target_dependencies(witmotion_ros_node Qt5Core)

install(
  TARGETS witmotion_ros_node
  ARCHIVE DESTINATION lib/${PROJECT_NAME}
  LIBRARY DESTINATION lib/${PROJECT_NAME}
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
install(DIRECTORY config DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
