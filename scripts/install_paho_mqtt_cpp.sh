git clone https://github.com/eclipse/paho.mqtt.cpp
cd paho.mqtt.cpp
cmake -Bbuild -H.
sudo cmake --build build/ --target install
sudo ldconfig
