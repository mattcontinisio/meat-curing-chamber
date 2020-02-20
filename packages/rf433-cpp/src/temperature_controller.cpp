#include "mqtt_client.hpp"

#include "INIReader.h"
#include "cxxopts.hpp"

#include <RCSwitch.h>
#include <mqtt/client.h>
#include <spdlog/spdlog.h>

#include <string>
#include <utility>
#include <vector>

int main(int argc, char* argv[]) {
    cxxopts::Options options("temperature_controller", "Controls fridge temperature");
    options.add_options()("c,config", "path to config file",
                          cxxopts::value<std::string>()->default_value("config.ini"))(
        "h,help", "show this help message and exit");
    const auto args = options.parse(argc, argv);

    if (args.count("help")) {
        std::cout << options.help() << std::endl;
        return 0;
    }

    const INIReader config{args["config"].as<std::string>()};
    if (config.ParseError() != 0) {
        spdlog::error("Failed to load 'config.ini', error={}", config.ParseError());
        return 1;
    }

    const auto temperature_range =
        std::make_pair(config.GetFloat("temperature", "low", -1), config.GetFloat("temperature", "high", -1));

    if (wiringPiSetup() == -1) {
        spdlog::error("wiringPiSetup() failed");
        return 1;
    }

    RCSwitch rcSwitch;
    rcSwitch.setProtocol(1);
    const auto pulse = config.GetInteger("rf433", "pulse", -1);
    if (pulse > 0) {
        rcSwitch.setPulseLength(pulse);
    }
    rcSwitch.enableTransmit(config.GetInteger("rf433", "tx_pin", -1));

    // mqtt
    const auto broker_host = config.Get("mqtt", "broker_host", "localhost'");
    const auto broker_port = config.GetInteger("mqtt", "broker_port", 1883);
    const std::string broker_address = "tcp://" + broker_host + ":" + std::to_string(broker_port);

    const auto location = config.Get("mqtt", "location", "unknown");
    const std::string client_id = location + "/temperature_controller_cpp";
    const std::string temperature_topic = location + "/temperature";
    const std::vector<std::string> topics = {temperature_topic};

    miot::mqtt_client client{broker_address, client_id, topics};

    while (true) {
        spdlog::info("waiting for message");
        const auto msg = client.consume_message();
        if (!msg) {
            // todo reconnect
            spdlog::error("invalid message");
            continue;
        }

        const auto& topic = msg->get_topic();

        if (topic == temperature_topic) {
            spdlog::info("temperature={}", msg->to_string());
            const auto temperature = std::stof(msg->to_string());
            if (temperature < temperature_range.first) {
                spdlog::info("temperature is too low, turning off fridge");
                const auto code = config.GetInteger("rf433", "turn_off_fridge_code", -1);
                rcSwitch.send(code, 24);
            } else if (temperature > temperature_range.second) {
                spdlog::info("temperature is too high, turning on fridge");
                const auto code = config.GetInteger("rf433", "turn_on_fridge_code", -1);
                rcSwitch.send(code, 24);
            }
        } else {
            spdlog::warn("unexpected topic, topic={}", topic);
        }
    }

    return 0;
}
