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
    cxxopts::Options options("humidity_controller", "Controls humidifier");
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

    const auto humidity_range =
        std::make_pair(config.GetFloat("humidity", "low", -1), config.GetFloat("humidity", "high", -1));

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
    const std::string client_id = location + "/humidity_controller_cpp";
    const std::string humidity_topic = location + "/humidity";
    const std::vector<std::string> topics = {humidity_topic};

    miot::mqtt_client client{broker_address, client_id, topics};

    spdlog::info("mqtt client connected, client_id={}, location={}", client_id, location);

    while (true) {
        spdlog::info("waiting for message");
        const auto msg = client.consume_message();
        if (!msg) {
            // todo reconnect
            spdlog::error("invalid message");
            continue;
        }

        const auto& topic = msg->get_topic();

        if (topic == humidity_topic) {
            spdlog::info("humidity={}", msg->to_string());
            const auto humidity = std::stof(msg->to_string());
            if (humidity < humidity_range.first) {
                const auto code = config.GetInteger("rf433", "turn_on_humidifier_code", -1);
                spdlog::info("humidity is too low, turning on humidifier with code={}", code);
                rcSwitch.send(code, 24);
            } else if (humidity > humidity_range.second) {
                const auto code = config.GetInteger("rf433", "turn_off_humidifier_code", -1);
                spdlog::info("humidity is too high, turning off humidifier with code={}", code);
                rcSwitch.send(code, 24);
            }
        } else {
            spdlog::warn("unexpected topic, topic={}", topic);
        }
    }

    return 0;
}
