from .rf433 import Rf433Device

import paho.mqtt.client as mqtt

import argparse, configparser, logging
logger = logging.getLogger(__name__)


def main():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fh = logging.FileHandler('humidity_controller.log')
    fh.setLevel(logging.DEBUG)
    logging.basicConfig(
        handlers=[ch, fh],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('humidity_controller')

    parser = argparse.ArgumentParser(description='Controls humidifier')
    parser.add_argument('-c',
                        '--config',
                        help='path to config file',
                        default='config.ini')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)
    if not config.read(args.config):
        logger.warn('failed to read config file, path={}'.format(args.config))

    location = config.get('mqtt', 'location', fallback='unknown')
    humidity_topic = '/'.join((location, 'humidity'))

    humidity_range = (config.getfloat('humidity', 'low'),
                      config.getfloat('humidity', 'high'))

    tx_device = Rf433Device(config.getint('rf433', 'tx_pin'),
                            config.getint('rf433', 'pulse'))

    # Connect to MQTT broker and subscribe
    def on_connect(client, userdata, flags, rc):
        logger.info('connected to mqtt broker')
        client.subscribe(humidity_topic)

    def on_humidity(client, userdata, msg):
        humidity = msg.payload
        if humidity < humidity_range[0]:
            logger.info('humidity is too low')
            tx_device.send(config.getint('rf433', 'turn_on_humidifier_code'))
        elif humidity > humidity_range[1]:
            logger.info('humidity is too high')
            tx_device.send(config.getint('rf433', 'turn_off_humidifier_code'))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.message_callback_add(humidity_topic, on_humidity)
    host = config.get('mqtt', 'broker_host', fallback='localhost')
    port = config.getint('mqtt', 'broker_port', fallback=1883)
    client.connect(host, port)
    client.loop_forever()


if __name__ == '__main__':
    main()
