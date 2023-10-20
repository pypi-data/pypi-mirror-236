cmake_minimum_required(VERSION 3.25)

project(roboflex_realsense VERSION 0.1.0 DESCRIPTION "roboflex realsense2 sensor")

# specify the C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)


# -------------------- 
# Resolve dependencies

# roboflex core
find_package(roboflex_core REQUIRED)

# Realsense2: we'd like to use whatever
# the user has installed, but fetch and 
# build it if they don't have it.

# ... it seems to cause problems ...
# find_package(realsense2 QUIET)
# if(NOT realsense2_FOUND)

    # Include FetchContent Module
    include(FetchContent)

    # realsense doesn't compile with c++20 urg 
    set(CMAKE_CXX_STANDARD 11)

    # Set desired cache variables for librealsense build
    set(BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
    set(BUILD_GRAPHICAL_EXAMPLES OFF CACHE BOOL "" FORCE)

    FetchContent_Declare(
        realsense2
        GIT_REPOSITORY https://github.com/IntelRealSense/librealsense.git
        GIT_TAG        v2.54.2
        #GIT_TAG        master
    )
    FetchContent_MakeAvailable(realsense2)

    set(CMAKE_CXX_STANDARD 20)
#endif()



# -------------------- 
# Define the library

add_library(roboflex_realsense STATIC
    src/realsense.cpp
    include/roboflex_realsense/realsense.h
)

# Set some properties on our library
set_property(TARGET roboflex_realsense PROPERTY 
    POSITION_INDEPENDENT_CODE ON
)

# Include directories when we compile our library
target_include_directories(roboflex_realsense PUBLIC 
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include> 
    $<INSTALL_INTERFACE:include>
    ${xtensor_INCLUDE_DIRS}
)

# Link against the necessary libraries
target_link_libraries(roboflex_realsense PUBLIC 
    roboflex_core::roboflex_core 
    realsense2
)


# -------------------- 
# Examples

# run_realsense_cpp example
add_executable(run_realsense_cpp examples/run_realsense_cpp.cpp)
target_link_libraries(run_realsense_cpp PRIVATE 
    roboflex_core::roboflex_core 
    roboflex_realsense
)


# -------------------- 
# install

# If you need to install the realsense library
install(TARGETS roboflex_realsense 
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
)
install(DIRECTORY include/roboflex_realsense
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
