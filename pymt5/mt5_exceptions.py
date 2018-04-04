

class MT5Error(Exception):
    """
    Base error
    """
    pass


class MT5ConnectionError(MT5Error):
    """
    Connection errors
    """
    pass


class MT5SocketError(MT5Error):
    """
    Socket operations error (send, recv)
    """
    pass

