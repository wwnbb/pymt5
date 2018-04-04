import json

from .mt5_logger import MT5Logger
from .mt5_connect import MT5Connect
from .mt5_protocol import MT5ReturnCodes


class MT5Group(object):

    CMD_GROUP_GET = 'GROUP_GET'
    CMD_GROUP_ADD = 'GROUP_ADD'
    CMD_GROUP_DELETE = 'GROUP_DELETE'
    CMD_GROUP_TOTAL = 'GROUP_TOTAL'
    CMD_GROUP_NEXT = 'GROUP_NEXT'

    PARAM_GROUP = 'GROUP'

    connect = None

    def __init__(self, connect, log_level='ERROR'):
        """
        Init group module
        :param connect:
        :type connect: MT5Connect
        """
        self.logger = MT5Logger(self.__class__.__name__, level=log_level)
        self.connect = connect

    def get(self, group):
        """
        Get group
        :return:
        """
        if not self.connect.send(self.CMD_GROUP_GET, {
            self.PARAM_GROUP: group
        }):
            self.logger.error("Get group failed")
            return False

        try:
            header, body = self.connect.read()
        except TypeError:
            self.logger.error("Read group failed")
            return False

        if MT5ReturnCodes.PARAM not in body.options \
                or body.data is None \
                or body.options[MT5ReturnCodes.PARAM] != MT5ReturnCodes.STATUS_DONE:
            self.logger.error("Get group failed")
            return False

        return json.loads(body.data)

    def add(self):
        pass

    def delete(self):
        pass

    def get_total(self):
        pass

    def get_next(self):
        pass

    def get_all(self):
        pass
