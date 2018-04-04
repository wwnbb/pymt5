import sys
import logging
from logging import StreamHandler


class MT5Logger(object):

    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR
    }

    __name = None
    __logger = None

    def __init__(self, name='', level='DEBUG'):
        """
        Init logger class
        :param name: Logger name
        :type name: str
        """

        self.__name = name
        self.__logger = logging.getLogger(self.__name)
        self.__logger.setLevel(self.levels[level])
        stream_handler = StreamHandler(stream=sys.stderr)
        formatter = logging.Formatter('%(asctime)s [%(name)s/%(levelname)s]: %(message)s')
        stream_handler.setFormatter(formatter)
        self.__logger.addHandler(stream_handler)

    def debug(self, message):
        """
        Debug message
        :param message:
        :type message: str
        :return:
        """
        self.__logger.debug(message)

    def info(self, message):
        """
        Info message
        :param message:
        :type message: str
        :return:
        """
        self.__logger.info(message)

    def warning(self, message):
        """
        Warning message
        :param message:
        :type message: str
        :return:
        """
        self.__logger.warning(message)

    def error(self, message):
        """
        Error message
        :param message:
        :type message: str
        :return:
        """
        self.__logger.error(message)
