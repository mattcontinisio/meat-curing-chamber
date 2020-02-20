import paho.mqtt.client as mqtt
import slack

import argparse, configparser, logging, os
logger = logging.getLogger(__name__)


def main():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fh = logging.FileHandler('slack.log')
    fh.setLevel(logging.DEBUG)
    logging.basicConfig(
        handlers=[ch, fh],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('slack')

    parser = argparse.ArgumentParser(
        description='Posts messages to slack channel')
    parser.add_argument('-c',
                        '--config',
                        help='path to config file',
                        default='config.ini')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    if not config.read(args.config):
        logger.warn('failed to read config file, path={}'.format(args.config))

    location = config.get('mqtt', 'location', fallback='unknown')
    channel = config.get('slack', 'channel')
    logger.info('starting, location={}, channel={}'.format(location, channel))

    slack_client = slack.WebClient(token=os.environ['SLACK_ACCESS_TOKEN'])

    def on_connect(client, userdata, flags, rc):
        logger.info('connected to mqtt broker')
        topic = '/'.join((location, '#'))
        client.subscribe(topic)

        slack_client.chat_postMessage(
            channel=channel, text='Meat curing chamber slack alerter started')

    client = mqtt.Client()
    client.on_connect = on_connect
    host = config.get('mqtt', 'broker_host', fallback='localhost')
    port = config.getint('mqtt', 'broker_port', fallback=1883)
    client.connect(host, port)
    client.loop_forever()


if __name__ == '__main__':
    main()
