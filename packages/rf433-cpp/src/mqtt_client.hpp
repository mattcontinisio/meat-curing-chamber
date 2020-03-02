#pragma once

#include <mqtt/client.h>

#include <string>
#include <vector>

namespace miot {

// Wrap mqtt::client
// connect and subscribe in constructor
// disconnect in destructor
class mqtt_client {
public:
    mqtt_client(const std::string& broker_address, const std::string& client_id,
                const std::vector<std::string>& topics);
    ~mqtt_client();

    // Get reference to underlying client
    mqtt::client& get();

private:
    mqtt::client client_;
};

} // namespace miot
