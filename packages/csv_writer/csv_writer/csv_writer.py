import paho.mqtt.client as mqtt

import argparse, configparser, csv, datetime, logging, time
logger = logging.getLogger(__name__)


def main():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fh = logging.FileHandler('csv_writer.log')
    fh.setLevel(logging.DEBUG)
    logging.basicConfig(
        handlers=[ch, fh],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('csv_writer')

    parser = argparse.ArgumentParser(
        description='Writes humidity and temperature data to CSV file')
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

    filename = 'readings-{}.csv'.format(time.time())
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['time', 'humidity', 'temperature'])

    def on_connect(client, userdata, flags, rc):
        logger.info('connected to mqtt broker')
        topic = '/'.join((location, '#'))
        client.subscribe(topic)

    def on_humidity(client, userdata, msg):
        humidity = msg.payload
        logger.debug('writing humidity={}'.format(humidity))
        with open(filename, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            now = datetime.datetime.now().isoformat()
            writer.writerow([now, humidity, ''])

    def on_temperature(client, userdata, msg):
        temperature = msg.payload
        logger.debug('writing temperature={}'.format(temperature))
        with open(filename, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            now = datetime.datetime.now().isoformat()
            writer.writerow([now, '', temperature])

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
