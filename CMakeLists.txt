cmake_minimum_required(VERSION 3.5)
project(meat-curing-chamber CXX)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DRPI")
set(CMAKE_CXX_STANDARD 11)

option(USE_RC_SWITCH_MOCK "" OFF)
option(BUILD_CXXOPTS "" ON)
option(BUILD_PAHO_MQTT "" OFF)
option(BUILD_SPDLOG "" OFF)

find_package(Threads REQUIRED)
find_package(OpenSSL REQUIRED)
find_package(PahoMqttCpp REQUIRED)
find_package(spdlog REQUIRED)
find_library(wiringPi wiringPi)
find_library(wiringPiDev wiringPiDev)

#deps
if(BUILD_CXXOPTS)
    set(CXXOPTS_DEPS_DIR ${meat-curing-chamber_SOURCE_DIR}/deps/cxxopts)
    configure_file(${meat-curing-chamber_SOURCE_DIR}/cmake/in/cxxopts.in ${CXXOPTS_DEPS_DIR}/CMakeLists.txt)
    execute_process(COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" . WORKING_DIRECTORY ${CXXOPTS_DEPS_DIR})
    execute_process(COMMAND ${CMAKE_COMMAND} --build . WORKING_DIRECTORY ${CXXOPTS_DEPS_DIR})
endif()

if(BUILD_PAHO_MQTT)
    set(PAHO_MQTT_C_DEPS_DIR ${meat-curing-chamber_SOURCE_DIR}/deps/paho_mqtt_c)
    configure_file(${meat-curing-chamber_SOURCE_DIR}/cmake/in/paho_mqtt_c.in ${PAHO_MQTT_C_DEPS_DIR}/CMakeLists.txt)
    execute_process(COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" . WORKING_DIRECTORY ${PAHO_MQTT_C_DEPS_DIR})
    execute_process(COMMAND ${CMAKE_COMMAND} --build . WORKING_DIRECTORY ${PAHO_MQTT_C_DEPS_DIR})
    add_subdirectory(${PAHO_MQTT_C_DEPS_DIR}/src)

    set(PAHO_MQTT_CPP_DEPS_DIR ${meat-curing-chamber_SOURCE_DIR}/deps/paho_mqtt_cpp)
    configure_file(${meat-curing-chamber_SOURCE_DIR}/cmake/in/paho_mqtt_cpp.in ${PAHO_MQTT_CPP_DEPS_DIR}/CMakeLists.txt)
    execute_process(COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" . WORKING_DIRECTORY ${PAHO_MQTT_CPP_DEPS_DIR})
    execute_process(COMMAND ${CMAKE_COMMAND} --build . WORKING_DIRECTORY ${PAHO_MQTT_CPP_DEPS_DIR})
    add_subdirectory(${PAHO_MQTT_CPP_DEPS_DIR}/src)
endif()

if(USE_RC_SWITCH_MOCK)
    set(RC_SWITCH_DEPS_DIR ${meat-curing-chamber_SOURCE_DIR}/deps/rc_switch_mock)
else()
    set(RC_SWITCH_DEPS_DIR ${meat-curing-chamber_SOURCE_DIR}/deps/rc_switch)
    configure_file(${meat-curing-chamber_SOURCE_DIR}/cmake/in/rc_switch.in ${RC_SWITCH_DEPS_DIR}/CMakeLists.txt)
    execute_process(COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" . WORKING_DIRECTORY ${RC_SWITCH_DEPS_DIR})
    execute_process(COMMAND ${CMAKE_COMMAND} --build . WORKING_DIRECTORY ${RC_SWITCH_DEPS_DIR})
endif()
add_library(rc-switch
    ${RC_SWITCH_DEPS_DIR}/src/RCSwitch.cpp
    ${RC_SWITCH_DEPS_DIR}/src/RCSwitch.h
)
set_target_properties(rc-switch PROPERTIES LINKER_LANGUAGE CXX)

if(BUILD_SPDLOG)
    set(SPDLOG_DEPS_DIR ${meat-curing-chamber_SOURCE_DIR}/deps/spdlog)
    configure_file(${meat-curing-chamber_SOURCE_DIR}/cmake/in/spdlog.in ${SPDLOG_DEPS_DIR}/CMakeLists.txt)
    execute_process(COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" . WORKING_DIRECTORY ${SPDLOG_DEPS_DIR})
    execute_process(COMMAND ${CMAKE_COMMAND} --build . WORKING_DIRECTORY ${SPDLOG_DEPS_DIR})
    add_subdirectory(${SPDLOG_DEPS_DIR}/src)
endif()

add_subdirectory(packages/rf433-cpp)
