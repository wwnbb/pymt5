
from hashlib import md5
from random import randrange


class MT5Utils(object):

    @staticmethod
    def get_hash_from_password(password):
        """
        Get hash password
        :param password:
        :type password: str
        :return:
        """
        return md5(md5(password.encode('utf-16le')).digest() + b'WebAPI').hexdigest()

    @staticmethod
    def get_random_hex(length):
        """
        Generate random hex string
        :param length:
        :return:
        """
        return ''.join("%02x" % randrange(0, 254) for i in range(0, length))

    @staticmethod
    def quotes(data):
        """
        Replace special chars
        :param data:
        :type data: str
        :return:
        """

        replaces = (('\\', '\\\\'), ('=', '\='), ('|', '\|'), ('\r', '\\r'), ('\n', '\\n'), )

        for key, val in replaces:
            data = data.replace(key, val)

        return data
