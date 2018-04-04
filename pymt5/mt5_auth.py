from hashlib import md5

from .mt5_logger import MT5Logger
from .mt5_connect import MT5Connect
from .mt5_protocol import VERSION, MT5ReturnCodes
from .mt5_crypt import MT5Crypt
from .mt5_utils import MT5Utils


class MT5Auth(object):

    CMD_AUTH_START = 'AUTH_START'
    CMD_AUTH_ANSWER = 'AUTH_ANSWER'

    PARAM_AGENT = 'AGENT'
    PARAM_VERSION = 'VERSION'
    PARAM_TYPE = 'TYPE'
    PARAM_LOGIN = 'LOGIN'
    PARAM_SRV_RAND = 'SRV_RAND'
    PARAM_SRV_RAND_ANSWER = 'SRV_RAND_ANSWER'
    PARAM_CLI_RAND = 'CLI_RAND'
    PARAM_CLI_RAND_ANSWER = 'CLI_RAND_ANSWER'
    PARAM_CRYPT_RAND = 'CRYPT_RAND'
    PARAM_CRYPT_METHOD = 'CRYPT_METHOD'

    VAL_CRYPT_NONE = "NONE"
    VAL_CRYPT_AES256OFB = "AES256OFB"

    connect = None
    agent = None

    def __init__(self, connect, log_level='ERROR', agent='PYMT5'):
        """
        Init
        :param connect:
        :type connect: MT5Connect
        :param agent:
        :type agent: str
        """
        self.logger = MT5Logger(self.__class__.__name__, level=log_level)

        self.connect = connect
        self.agent = agent

    def auth(self, login, password):
        """
        Auth to MT5 server
        :param login:
        :type login: str
        :param password:
        :type password: str
        :return:
        :rtype: bool
        """

        """
        Auth start
        """
        if not self.connect.send(self.CMD_AUTH_START, {
            self.PARAM_VERSION: VERSION,
            self.PARAM_AGENT: self.agent,
            self.PARAM_LOGIN: login,
            self.PARAM_TYPE: 'MANAGER',
            self.PARAM_CRYPT_METHOD:
                self.VAL_CRYPT_AES256OFB if self.connect.is_crypt else self.VAL_CRYPT_NONE
        }):
            self.logger.error("Send auth data failed")
            return False

        try:
            header, body = self.connect.read()
        except TypeError:
            self.logger.error("Read auth data failed")
            return False

        """
        Check status auth start command
        """
        if MT5ReturnCodes.PARAM not in body.options \
                or self.PARAM_SRV_RAND not in body.options \
                or body.options[MT5ReturnCodes.PARAM] != MT5ReturnCodes.STATUS_DONE:
            self.logger.error("Auth failed")
            return False

        """
        Auth answer
        """
        cli_rand = MT5Utils.get_random_hex(16)

        pass_hash = MT5Utils.get_hash_from_password(password)

        srv_rand_answ = md5(
            bytes.fromhex(pass_hash) +
            bytes.fromhex(body.options[self.PARAM_SRV_RAND])).hexdigest()

        if not self.connect.send(self.CMD_AUTH_ANSWER, {
            self.PARAM_SRV_RAND_ANSWER: srv_rand_answ,
            self.PARAM_CLI_RAND: cli_rand
        }):
            self.logger.error("Send auth data failed")
            return False

        try:
            header, body = self.connect.read()
        except TypeError:
            self.logger.error("Read auth data failed")
            return False

        """
        Check auth user answer
        """
        if MT5ReturnCodes.PARAM not in body.options \
                or self.PARAM_CLI_RAND_ANSWER not in body.options \
                or body.options[MT5ReturnCodes.PARAM] != MT5ReturnCodes.STATUS_DONE:
            self.logger.error("Auth failed")
            return False

        cli_rand_answ = md5(
            bytes.fromhex(pass_hash) +
            bytes.fromhex(cli_rand)).hexdigest()

        if body.options[self.PARAM_CLI_RAND_ANSWER] != cli_rand_answ:
            self.logger.error("Server return broken password hash")
            return False

        if self.PARAM_CRYPT_RAND in body.options and body.options[self.PARAM_CRYPT_RAND]:
            self.connect.crypt = MT5Crypt(body.options[self.PARAM_CRYPT_RAND], pass_hash)

        return True


