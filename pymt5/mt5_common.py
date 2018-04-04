import json

from .mt5_logger import MT5Logger
from .mt5_connect import MT5Connect
from .mt5_protocol import MT5ReturnCodes


class MT5Common(object):

    CMD_COMMON_GET = 'COMMON_GET'

    connect = None

    def __init__(self, connect, log_level='ERROR'):
        """
        Init common module
        :param connect:
        :type connect: MT5Connect
        """
        self.logger = MT5Logger(self.__class__.__name__, level=log_level)
        self.connect = connect

    def get(self):
        """
        Get common information
        :return:
        """

        if not self.connect.send(self.CMD_COMMON_GET, {}):
            self.logger.error("Get common information failed")
            return False

        try:
            header, body = self.connect.read()
        except TypeError:
            self.logger.error("Read common information failed")
            return False

        if MT5ReturnCodes.PARAM not in body.options \
                or body.data is None \
                or body.options[MT5ReturnCodes.PARAM] != MT5ReturnCodes.STATUS_DONE:
            self.logger.error("Get common information failed")
            return False

        return json.loads(body.data)
