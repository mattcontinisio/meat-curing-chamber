# ubuntu cpp

FROM ubuntu:eoan

WORKDIR /tmp

RUN echo "*** Installing dependencies ***" \
  && apt-get update \
  && apt-get dist-upgrade -y \
  && apt-get install -y apt-utils curl git vim \
  && apt-get install -y cmake g++-7 \
  && apt-get install -y libssl-dev libwiringpi-dev wiringpi \
  && apt-get autoremove --purge -y \
  && apt-get autoclean -y \
  && rm -rf /var/cache/apt/* /tmp/* \
  && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 1

RUN echo "** Installing Paho MQTT C ***" \
  && git clone https://github.com/eclipse/paho.mqtt.c.git \
  && cd paho.mqtt.c \
  && git checkout v1.3.1 \
  && cmake -Bbuild -H. -DPAHO_WITH_SSL=ON -DPAHO_ENABLE_TESTING=OFF \
  && cmake --build build/ --target install \
  && ldconfig \
  && cd .. \
  && rm -rf paho.mqtt.c

RUN echo "** Installing Paho MQTT CPP ***" \
  && git clone https://github.com/eclipse/paho.mqtt.cpp \
  && cd paho.mqtt.cpp \
  && cmake -Bbuild -H. \
  && cmake --build build/ --target install \
  && ldconfig \
  && cd .. \
  && rm -rf paho.mqtt.cpp

RUN echo "** Installing spdlog ***" \
  && git clone https://github.com/gabime/spdlog.git \
  && cd spdlog \
  && git checkout v1.5.0 \
  && mkdir build \
  && cd build \
  && cmake -DSPDLOG_BUILD_EXAMPLE=OFF -DSPDLOG_BUILD_TESTS=OFF .. \
  && make -j \
  && make install \
  && ldconfig \
  && cd ../.. \
  && rm -rf spdlog

WORKDIR /build
