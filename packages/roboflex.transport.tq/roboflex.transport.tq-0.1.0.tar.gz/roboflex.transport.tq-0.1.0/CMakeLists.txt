cmake_minimum_required(VERSION 3.25)

project(roboflex_transport_tq VERSION 0.1.0 DESCRIPTION "roboflex webcamuvc")

# specify the C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)


# -------------------- 
# Resolve dependencies

find_package(roboflex_core REQUIRED)


# -------------------- 
# Define the library

add_library(roboflex_transport_tq STATIC
    src/tq.cpp
    include/roboflex_transport_tq/tq.h
)

# Set some properties on our library
set_property(TARGET roboflex_transport_tq PROPERTY 
    POSITION_INDEPENDENT_CODE ON
)

# Include directories when we compile our library
target_include_directories(roboflex_transport_tq PUBLIC 
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include> 
    $<INSTALL_INTERFACE:include>
)

# Link against the necessary libraries
target_link_libraries(roboflex_transport_tq PUBLIC 
    roboflex_core::roboflex_core 
)


# -------------------- 
# install

# If you need to install the transport_tq library
install(TARGETS roboflex_transport_tq 
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
)
#install(FILES tq.h DESTINATION include/roboflex_transport_tq)
install(DIRECTORY include/roboflex_transport_tq
    DESTINATION include
)


# --------------------
# build python bindings

add_subdirectory(python)
