cmake_minimum_required(VERSION 3.3 FATAL_ERROR)
project(openmc_sources CXX)

# Explicitly set OpenMC path for the container environment
set(OpenMC_DIR "/opt/openmc/lib/cmake/openmc")

add_library(pu238_source SHARED pu238_source.cpp)
find_package(OpenMC REQUIRED)
target_link_libraries(pu238_source OpenMC::libopenmc)