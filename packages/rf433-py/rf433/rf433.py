import logging
logger = logging.getLogger(__name__)

from enum import Enum
import time

try:
    import rpi_rf
except ImportError:
    logger.error('error importing rpi_rf, using mock')
    from . import mock_rpi_rf as rpi_rf


class Rf433Device:
    def __init__(self, pin: int, pulse: int):
        self.pulse = pulse

        self.rf_device = rpi_rf.RFDevice(pin)
        self.rf_device.enable_tx()

    def __del__(self):
        self.rf_device.cleanup()

    def send(self, code: int):
        logger.debug('sending code={}'.format(code))
        self.rf_device.tx_code(code, 1, self.pulse, 24)
