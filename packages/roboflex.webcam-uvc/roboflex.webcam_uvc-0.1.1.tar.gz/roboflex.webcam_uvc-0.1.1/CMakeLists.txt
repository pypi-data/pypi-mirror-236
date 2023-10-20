cmake_minimum_required(VERSION 3.25)

project(roboflex_webcam_uvc VERSION 0.1.1 DESCRIPTION "roboflex webcamuvc")

# specify the C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)


# -------------------- 
# Resolve dependencies

# Include FetchContent Module
include(FetchContent)

# Fetch and make libuvc available
FetchContent_Declare(
  libuvc
  GIT_REPOSITORY https://github.com/libuvc/libuvc.git
  GIT_TAG        origin/master
)
FetchContent_MakeAvailable(libuvc)

# Locate the installed roboflex_core and its dependencies
find_package(roboflex_core REQUIRED)


# -------------------- 
# Define the library

add_library(roboflex_webcam_uvc STATIC
    src/webcam_uvc.cpp
    include/roboflex_webcam_uvc/webcam_uvc.h
)

# Set some properties on our library
set_property(TARGET roboflex_webcam_uvc PROPERTY 
    POSITION_INDEPENDENT_CODE ON
)

# Include directories when we compile our library
target_include_directories(roboflex_webcam_uvc PUBLIC 
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include> 
    $<INSTALL_INTERFACE:include>
    ${xtensor_INCLUDE_DIRS}
)

# Link against the necessary libraries
target_link_libraries(roboflex_webcam_uvc PUBLIC 
    roboflex_core::roboflex_core 
    uvc
)


# -------------------- 
# Examples

# run_webcam_cpp example
add_executable(run_webcam_cpp examples/run_webcam_cpp.cpp)
target_link_libraries(run_webcam_cpp PRIVATE roboflex_core::roboflex_core roboflex_webcam_uvc)


# -------------------- 
# install

# If you need to install the webcam_uvc library
install(TARGETS roboflex_webcam_uvc 
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
)
#install(FILES webcam_uvc.h DESTINATION include/roboflex_webcam_uvc)
install(DIRECTORY include/roboflex_webcam_uvc
    DESTINATION include
)


# --------------------
# build python bindings

add_subdirectory(python)


# Not sure when we should do ExternalProject_Add vs find_package:
#
# include(ExternalProject)
# ExternalProject_Add(
#     roboflex_core
#     PREFIX ${CMAKE_BINARY_DIR}/_deps
#     SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../roboflex_core
#     CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=<INSTALL_DIR>
#     #CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${CMAKE_CURRENT_SOURCE_DIR}/../roboflex_core
#     #CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${CMAKE_CURRENT_SOURCE_DIR}/../roboflex_core/build/output_tst
# )

# # Get the source directory of the external project roboflex_core
# ExternalProject_Get_Property(roboflex_core SOURCE_DIR)
