add_executable(unit_tests bytes_test.cc)

target_link_libraries(
    unit_tests
    PRIVATE ${TARGET_NAME}::${TARGET_NAME} Catch2::Catch2WithMain
)
target_include_directories(unit_tests PRIVATE ${CMAKE_SOURCE_DIR})

include(FetchContent)

fetchcontent_declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG
        v3.4.0 # or a later release
)

fetchcontent_makeavailable(Catch2)

include(CTest)
include(Catch)
catch_discover_tests(unit_tests)
