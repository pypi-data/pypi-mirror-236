cmake_minimum_required(VERSION 3.15)
project(WaveletBufferTest CXX)

find_package(drift_bytes CONFIG REQUIRED)

add_executable(example src/example.cc)
target_compile_features(example PUBLIC cxx_std_17)
target_link_libraries(example drift_bytes::drift_bytes)
