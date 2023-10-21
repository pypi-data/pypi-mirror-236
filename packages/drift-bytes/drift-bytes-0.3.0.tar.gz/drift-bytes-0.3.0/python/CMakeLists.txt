cmake_minimum_required(VERSION 3.16)
project(drift_bytes_py DESCRIPTION "DriftBytes Python binding")

# Include wavelet_buffer
add_subdirectory(../ ../)

if(SKBUILD)
    # Scikit-Build does not add your site-packages to the search path
    # automatically, so we need to add it _or_ the pybind11 specific directory
    # here.
    execute_process(
        COMMAND
            "${PYTHON_EXECUTABLE}" -c
            "import pybind11; print(pybind11.get_cmake_dir())"
        OUTPUT_VARIABLE _tmp_dir
        OUTPUT_STRIP_TRAILING_WHITESPACE
        COMMAND_ECHO STDOUT
    )
    list(APPEND CMAKE_PREFIX_PATH "${_tmp_dir}")
endif()

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(_drift_bytes MODULE
        src/main.cc
)

target_link_libraries(_drift_bytes PRIVATE drift_bytes::drift_bytes)
target_compile_definitions(
    _drift_bytes
    PRIVATE PYBIND11_DETAILED_ERROR_MESSAGES
)
target_include_directories(_drift_bytes PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/)
target_include_directories(_drift_bytes PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/..)

install(TARGETS _drift_bytes DESTINATION .)
