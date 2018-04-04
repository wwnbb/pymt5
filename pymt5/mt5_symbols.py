import json

from .mt5_logger import MT5Logger
from .mt5_connect import MT5Connect
from .mt5_protocol import MT5ReturnCodes


class MT5Symbols(object):

    CMD_SYMBOL_GET = 'SYMBOL_GET'
    CMD_SYMBOL_GET_GROUP = 'SYMBOL_GET_GROUP'
    CMD_SYMBOL_ADD = 'SYMBOL_ADD'
    CMD_SYMBOL_NEXT = 'SYMBOL_NEXT'
    CMD_SYMBOL_TOTAL = 'SYMBOL_TOTAL'

    PARAM_SYMBOL = 'SYMBOL'
    PARAM_GROUP = 'GROUP'
    PARAM_INDEX = 'INDEX'
    PARAM_TOTAL = 'TOTAL'

    connect = None

    def __init__(self, connect, log_level='ERROR'):
        """
        Init symbols module
        :param connect:
        :type connect: MT5Connect
        """
        self.logger = MT5Logger(self.__class__.__name__, level=log_level)
        self.connect = connect

    def get(self, symbol):
        """
        Get symbol by name
        :param symbol:
        :return:
        """
        if not self.connect.send(self.CMD_SYMBOL_GET, {
            self.PARAM_SYMBOL: symbol
        }):
            self.logger.error("Get symbol failed")
            return False

        try:
            header, body = self.connect.read()
        except TypeError:
            self.logger.error("Read symbol data failed")
            return False

        if MT5ReturnCodes.PARAM not in body.options \
                or body.data is None \
                or body.options[MT5ReturnCodes.PARAM] != MT5ReturnCodes.STATUS_DONE:
            self.logger.error("Get symbol failed")
            return False

        return json.loads(body.data)

    def get_group(self, symbol, group):
        """
        Get symbol by name and group
        :param symbol:
        :param group:
        :return:
        """
        if not self.connect.send(self.CMD_SYMBOL_GET_GROUP, {
            self.PARAM_SYMBOL: symbol,
            self.PARAM_GROUP: group
        }):
            self.logger.error("Get symbol failed")
            return False

        try:
            header, body = self.connect.read()
        except TypeError:
            self.logger.error("Read symbol data failed")
            return False

        if MT5ReturnCodes.PARAM not in body.options \
                or body.data is None \
                or body.options[MT5ReturnCodes.PARAM] != MT5ReturnCodes.STATUS_DONE:
            self.logger.error("Get symbol failed")
            return False

        return json.loads(body.data)

    def get_next(self, index=0):
        """
        Get symbol by index
        :param index:
        :type index: int
        :return:
        """

        if not self.connect.send(self.CMD_SYMBOL_NEXT, {
            self.PARAM_INDEX: index
        }):
            self.logger.error("Get symbol failed")
            return False

        try:
            header, body = self.connect.read()
        except TypeError:
            self.logger.error("Read symbol data failed")
            return False

        if MT5ReturnCodes.PARAM not in body.options \
                or body.data is None \
                or body.options[MT5ReturnCodes.PARAM] != MT5ReturnCodes.STATUS_DONE:
            self.logger.error("Get symbol failed")
            return False

        return json.loads(body.data)

    def add(self, data):
        """
        Set symbol data
        :param data:
        :return:
        """

        if not self.connect.send(self.CMD_SYMBOL_ADD, {}, json.dumps(data)):
            self.logger.error("Add symbol failed")
            return False

        try:
            header, body = self.connect.read()
        except TypeError:
            self.logger.error("Add data failed")
            return False

        if MT5ReturnCodes.PARAM not in body.options \
                or body.data is None \
                or body.options[MT5ReturnCodes.PARAM] != MT5ReturnCodes.STATUS_DONE:
            self.logger.error("Add symbol failed")
            return False

        return json.loads(body.data)

    def get_total(self):
        """
        Get total count symbols
        :return:
        """

        if not self.connect.send(self.CMD_SYMBOL_TOTAL, {}):
            self.logger.error("Get total symbols failed")
            return False

        try:
            header, body = self.connect.read()
        except TypeError:
            self.logger.error("Read symbol data failed")
            return False

        if MT5ReturnCodes.PARAM not in body.options \
                or self.PARAM_TOTAL not in body.options \
                or body.options[MT5ReturnCodes.PARAM] != MT5ReturnCodes.STATUS_DONE:
            self.logger.error("Get total symbols failed")
            return False

        return int(body.options[self.PARAM_TOTAL])

    def get_all(self):
        """
        Get all symbols
        :return:
        """

        result = []

        count = self.get_total()

        if count is False:
            self.logger.error("Get all symbols failed")
            return False

        for index in range(0, count):
            symbol = self.get_next(index)

            if symbol is False:
                self.logger.error("Get all symbols failed")
                return False

            result.append(symbol)

        return result
