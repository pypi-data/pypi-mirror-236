cmake_minimum_required(VERSION 3.25)

project(roboflex_transport_zmq VERSION 0.1.0 DESCRIPTION "roboflex transport zmq")

# specify the C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)


# -------------------- 
# Resolve dependencies

# # Include FetchContent Module
include(FetchContent)

# Fetch and make libuvc available
FetchContent_Declare(
  libzmq
  GIT_REPOSITORY https://github.com/zeromq/libzmq.git
  GIT_TAG        v4.3.5
)
FetchContent_MakeAvailable(libzmq)

#find_package(ZeroMQ REQUIRED)

# Locate the installed roboflex_core and its dependencies
find_package(roboflex_core REQUIRED)


# -------------------- 
# Define the library

add_library(roboflex_transport_zmq STATIC
    src/zmq_nodes.cpp
    include/roboflex_transport_zmq/zmq_nodes.h
)

# Set some properties on our library
set_property(TARGET roboflex_transport_zmq PROPERTY 
    POSITION_INDEPENDENT_CODE ON
)

# Include directories when we compile our library
target_include_directories(roboflex_transport_zmq PUBLIC 
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include> 
    $<INSTALL_INTERFACE:include>
)

# Link against the necessary libraries
target_link_libraries(roboflex_transport_zmq PUBLIC 
    roboflex_core::roboflex_core 
    libzmq-static
)


# -------------------- 
# Examples

# run_webcam_cpp example
add_executable(pub_sub_0_cpp examples/pub_sub_0_cpp.cpp)
target_link_libraries(pub_sub_0_cpp PRIVATE roboflex_core::roboflex_core roboflex_transport_zmq)


# -------------------- 
# install

# If you need to install the transport_zmq library
install(TARGETS roboflex_transport_zmq 
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
)
#install(FILES transport_zmq.h DESTINATION include/roboflex_transport_zmq)
install(DIRECTORY include/roboflex_transport_zmq
    DESTINATION include
)


# --------------------
# build python bindings

add_subdirectory(python)
