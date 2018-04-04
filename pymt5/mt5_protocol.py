import re

from .mt5_utils import MT5Utils


VERSION = 1755


class MT5HeaderProtocol(object):

    HEADER_LENGTH = 9

    body_size = None
    number_command = None
    flag = None

    format = '%04x%04x%1x'

    def __init__(self, body_size, number_command, flag=0):
        """
        Init header protocol
        :param body_size:
        :type body_size: int
        :param number_command:
        :type number_command: int
        :param flag:
        :type flag: int
        """

        self.body_size = body_size
        self.number_command = number_command
        self.flag = flag

    def __str__(self):
        return self.format % (self.body_size, self.number_command, self.flag)

    @staticmethod
    def parse(data):
        """
        Convert bytes to MTHeaderProtocol
        :param data:
        :return:
        :rtype: MT5HeaderProtocol or None
        """

        try:
            header = data.decode('ascii')
        except Exception:
            return None

        if len(data) != MT5HeaderProtocol.HEADER_LENGTH:
            return None

        return MT5HeaderProtocol(
            body_size=int(header[0:4], 16),
            number_command=int(header[4:8], 16),
            flag=int(header[8], 16)
        )

    @property
    def bytes(self):
        """
        Convert format
        :return:
        """

        return str(self).encode('ascii')


class MT5BodyProtocol(object):

    command = None
    options = None
    data = None

    def __init__(self, command=None, options=None, data=None):
        """
        Init body protocol
        :param command:
        :type command: str
        :param options:
        :type options: dict
        :param data:
        :type data: str
        """

        self.command = command
        self.options = options or {}
        self.data = data

    def __str__(self):

        result = self.command + '|'

        for key, val in self.options.items():
            result += key + '=' + MT5Utils.quotes(str(val)) + '|'

        if self.data:
            result += '\r\n' + self.data.replace('\r\n', ' ')

        return result

    @staticmethod
    def parse(sections):
        """
        Convert bytes to MTBodyProtocol
        :param sections:
        :return:
        """

        try:
            body = sections.decode('utf-16le').rstrip('\r\n\x00')
        except Exception:
            return None

        result = MT5BodyProtocol()

        sections = re.split(r'(?<!\\)\||(?<=\\{2})\|', body)
        result.command = sections[0] or None

        for option in sections[1:-1]:
            data = re.split(r'(?<!\\)=|(?<=\\{2})=', option, 1)
            result.options[data[0]] = data[1] if len(data) == 2 else 'NONE'

        result.data = sections[-1] or None

        return result

    @property
    def bytes(self):
        return (str(self) + '\r\n').encode('utf-16le')


class MT5ReturnCodes(object):
    """
    Command statuses
    """

    PARAM = 'RETCODE'
    STATUS_DONE = '0 Done'

