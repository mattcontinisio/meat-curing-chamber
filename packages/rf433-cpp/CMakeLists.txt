add_executable(humidity_controller src/humidity_controller.cpp)

target_link_libraries(humidity_controller
    PahoMqttCpp::paho-mqttpp3
    rc-switch
    spdlog::spdlog
    ${wiringPi}
    ${wiringPiDev}
    OpenSSL::SSL
    crypt
    rt
)

target_include_directories(humidity_controller PUBLIC
    ${RC_SWITCH_DEPS_DIR}/src
)

add_executable(temperature_controller src/temperature_controller.cpp)

target_link_libraries(temperature_controller
    PahoMqttCpp::paho-mqttpp3
    rc-switch
    spdlog::spdlog
    ${wiringPi}
    ${wiringPiDev}
    OpenSSL::SSL
    crypt
    rt
)

target_include_directories(temperature_controller PUBLIC
    ${RC_SWITCH_DEPS_DIR}/src
)
