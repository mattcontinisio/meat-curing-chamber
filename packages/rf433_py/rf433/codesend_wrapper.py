import logging
logger = logging.getLogger(__name__)

from enum import Enum
import subprocess

RF_COMMAND = '/home/pi/Code/433Utils/RPi_utils/codesend'


class CodesendWrapper:
    def __init__(self, pin: int, pulse: int):
        self.pin = pin
        self.pulse = pulse

    def send(self, code: int):
        logger.debug('sending code={}'.format(code))
        subprocess.call([RF_COMMAND, code])
