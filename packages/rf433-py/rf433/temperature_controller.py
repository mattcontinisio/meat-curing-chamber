from .rf433 import Rf433Device

import paho.mqtt.client as mqtt

import argparse, configparser, logging
logger = logging.getLogger(__name__)


def main():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fh = logging.FileHandler('temperature_controller.log')
    fh.setLevel(logging.DEBUG)
    logging.basicConfig(
        handlers=[ch, fh],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('temperature_controller')

    parser = argparse.ArgumentParser(description='Controls fridge temperature')
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
    temperature_topic = '/'.join((location, 'temperature'))

    temperature_range = (config.getfloat('temperature', 'low'),
                         config.getfloat('temperature', 'high'))

    tx_device = Rf433Device(config.getint('rf433', 'tx_pin'),
                            config.getint('rf433', 'pulse'))

    # Connect to MQTT broker and subscribe
    def on_connect(client, userdata, flags, rc):
        logger.info('connected to mqtt broker')
        client.subscribe(temperature_topic)

    def on_temperature(client, userdata, msg):
        logger.debug('on_temperature, payload={}'.format(msg.payload))
        temperature = float(msg.payload)
        if temperature < temperature_range[0]:
            logger.info('temperature is too low')
            tx_device.send(config.getint('rf433', 'turn_off_fridge_code'))
        elif temperature > temperature_range[1]:
            logger.info('temperature is too high')
            tx_device.send(config.getint('rf433', 'turn_on_fridge_code'))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.message_callback_add(temperature_topic, on_temperature)
    host = config.get('mqtt', 'broker_host', fallback='localhost')
    port = config.getint('mqtt', 'broker_port', fallback=1883)
    client.connect(host, port)
    client.loop_forever()


if __name__ == '__main__':
    main()
