#pragma once

#include <mqtt/client.h>
#include <spdlog/spdlog.h>

#include <iostream>
#include <string>
#include <vector>

namespace miot {

// Wrap mqtt::client
// connect and subscribe in constructor
// disconnect in destructor
class mqtt_client {
  public:
    mqtt_client(const std::string& broker_address, const std::string& client_id, const std::vector<std::string>& topics)
        : client_(broker_address, client_id) {
        mqtt::connect_options connect_options;
        connect_options.set_keep_alive_interval(20);
        connect_options.set_clean_session(false);
        const auto connect_response = client_.connect(connect_options);
        if (!connect_response.is_session_present()) {
            client_.subscribe(topics);
        } else {
            spdlog::info("Session already exists for this client");
        }
    }

    ~mqtt_client() { client_.disconnect(); }

    mqtt::const_message_ptr consume_message() { return client_.consume_message(); }

  private:
    mqtt::client client_;
};

} // namespace miot
