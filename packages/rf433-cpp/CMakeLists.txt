add_executable(humidity_controller
    src/humidity_controller.cpp
    src/mqtt_client.cpp
    src/mqtt_client.hpp
)

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
    ${CXXOPTS_DEPS_DIR}/src/include
    ${RC_SWITCH_DEPS_DIR}/src
)

add_executable(temperature_controller
    src/temperature_controller.cpp
    src/mqtt_client.cpp
    src/mqtt_client.hpp
)

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
    ${CXXOPTS_DEPS_DIR}/src/include
    ${RC_SWITCH_DEPS_DIR}/src
)
