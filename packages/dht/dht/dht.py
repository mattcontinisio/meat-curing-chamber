import paho.mqtt.client as mqtt
from schema import Schema, And, Use, Optional

import argparse, configparser, logging, sched, time
logger = logging.getLogger(__name__)

try:
    import Adafruit_DHT
except ImportError:
    logger.error('error importing Adafruit_DHT, using mock')
    from . import mock_Adafruit_DHT as Adafruit_DHT


class SensorReading:
    def __init__(self, humidity: float, temperature: float):
        self.humidity = humidity
        self.temperature = temperature

    def __str__(self):
        return "{{'humidity': {}%, 'temperature': {}°C}}".format(
            self.humidity, self.temperature)

    def is_valid(self):
        return self.humidity is not None and self.temperature is not None


class DhtSensor:
    def __init__(self, sensor_type: int, pin: int):
        self.sensor_type = sensor_type
        self.pin = pin

    def read(self):
        humidity, temperature = Adafruit_DHT.read(self.sensor_type, self.pin)
        if humidity is None or temperature is None:
            logger.error('Could not read humidity or temperature')

        return SensorReading(humidity, temperature)


def main():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fh = logging.FileHandler('dht.log')
    fh.setLevel(logging.DEBUG)
    logging.basicConfig(
        handlers=[ch, fh],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('dht')

    parser = argparse.ArgumentParser(
        description=
        'Publishes humidity and temperature data from Adafruit DHT series sensors'
    )
    parser.add_argument('-c',
                        '--config',
                        help='path to config file',
                        default='config.ini')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)
    if not config.read(args.config):
        logger.warn('failed to read config file, path={}'.format(args.config))

    config_schema = Schema(
        {
            'dht': {
                'type': Use(int),
                'pin': Use(int),
                Optional('read_interval', default=60): Use(int)
            },
            Optional('mqtt'): {
                Optional('broker_host', default='localhost'): str,
                Optional('broker_port', default='1883'): Use(int)
            }
        },
        ignore_extra_keys=True)
    config_schema.validate(config._sections)

    location = config.get('mqtt', 'location', fallback='unknown')
    humidity_topic = '/'.join((location, 'humidity'))
    temperature_topic = '/'.join((location, 'temperature'))

    # Create sensor
    sensor_type = config.getint('dht', 'type')
    pin = config.getint('dht', 'pin')
    sensor = DhtSensor(sensor_type, pin)

    def on_connect(client, userdata, flags, rc):
        logger.info('connected to mqtt broker')

    # Connect to MQTT broker
    client = mqtt.Client()
    client.on_connect = on_connect
    host = config.get('mqtt', 'broker_host', fallback='localhost')
    port = config.getint('mqtt', 'broker_port', fallback=1883)
    client.connect(host, port)
    client.loop_start()

    # Publish sensor readings
    read_interval = config.getint('dht', 'read_interval', fallback=60)
    logger.debug('read_interval={}'.format(read_interval))
    scheduler = sched.scheduler(time.time, time.sleep)

    def read():
        scheduler.enter(read_interval, 1, read)
        reading = sensor.read()
        if not reading.is_valid():
            return

        logger.debug(
            'publishing humidity={} and temperature={} for location={}'.format(
                reading.humidity, reading.temperature, location))

        client.publish(humidity_topic, reading.humidity)
        client.publish(temperature_topic, reading.temperature)

    read()
    scheduler.run()


if __name__ == '__main__':
    main()
