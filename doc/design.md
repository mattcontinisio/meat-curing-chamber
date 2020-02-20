# Meat curing chamber design

## Hardware

todo

## Software

![alt text](./architecture.png "Architecture")

The meat curing chamber is made up of different services and an MQTT message broker.

* dht - The `dht` service reads humidity and temperature data from a [DHT22 sensor](https://www.adafruit.com/product/385) and publishes the data to the topics:
    * `{location}/humidity`
    * `{location}/temperature`

  `{location}` is configurable. For example, `fridge.ini` sets it to `home/kitchen/fridge`.

* humidity_controller - The `humidity_controller` service subscribes to the `{location}/humidity` and turns a humidifier on/off based on a configurable humidity range. It uses an [RF433Mhz transmitter](https://www.electrodragon.com/product/433m-rf-wireless-transmitter-module/) to do this.  The humidifer is plugged into a [remote control outlet](https://www.etekcity.com/product/100068), which the RF433Mhz transmitter can turn on and off. There is a python and C++ version.

* temperature_controller - The `temperature_controller` service does the same thing as the `humidity_controller` but uses the `{location}/temperature` topic instead and controls a remote controler outlet that the fridge is plugged into. There is a python and C++ version.

### Other services

* csv_writer
* metrics
* slack
