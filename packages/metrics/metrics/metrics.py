import paho.mqtt.client as mqtt
from prometheus_client import start_http_server, Gauge

import argparse, configparser, logging
logger = logging.getLogger(__name__)

metrics = {
    'humidity': Gauge('humidity', 'Current humidity'),
    'temperature': Gauge('temperature', 'Current temperature')
}


def main():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fh = logging.FileHandler('metrics.log')
    fh.setLevel(logging.DEBUG)
    logging.basicConfig(
        handlers=[ch, fh],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('metrics')

    parser = argparse.ArgumentParser(
        description='Exposes metrics with Prometheus')
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

    start_http_server(config.getint('metrics', 'http_port', fallback=8000))

    def on_connect(client, userdata, flags, rc):
        logger.info('connected to mqtt broker')
        topic = '/'.join((location, '#'))
        client.subscribe(topic)

    def on_humidity(client, userdata, msg):
        humidity = msg.payload
        logger.debug('setting humidity={}'.format(humidity))
        metrics['humidity'].set(humidity)

    def on_temperature(client, userdata, msg):
        temperature = msg.payload
        logger.debug('setting temperature={}'.format(temperature))
        metrics['temperature'].set(temperature)

    client = mqtt.Client()
    client.on_connect = on_connect

    humidity_topic = '/'.join((location, '/humidity'))
    client.message_callback_add(humidity_topic, on_humidity)

    temperature_topic = '/'.join((location, '/temperature'))
    client.message_callback_add(temperature_topic, on_temperature)

    host = config.get('mqtt', 'broker_host', fallback='localhost')
    port = config.getint('mqtt', 'broker_port', fallback=1883)
    client.connect(host, port)
    client.loop_forever()


if __name__ == '__main__':
    main()
