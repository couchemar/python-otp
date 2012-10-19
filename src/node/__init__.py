# coding: utf-8
import logging
from gevent import sleep, socket, Greenlet


class OutgoingNodeConnection(Greenlet):
    logger = logging.getLogger('otp.node.connection')

    def __init__(self, port, cookie):
        self.port= port
        self.cookie = cookie

    def connect(self):
        try:
            self.socket = socket.create_conenction(('localhost',
                                                    self.port))
            self._connected = True
        except socket.error as exc:
            self.logger.error('Could not connect to %s', ('localhost',
                                                          self.port))

    def send_name(self):
        pass
