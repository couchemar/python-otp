# coding: utf-8
import logging
from gevent import socket, Greenlet
from node.protocol import encode_name, decode_status, decode_challenge


class OutgoingNodeConnection(Greenlet):
    logger = logging.getLogger('otp.node.connection')

    def __init__(self, node_name, port, cookie):
        super(OutgoingNodeConnection, self).__init__()
        self.port = port
        self.cookie = cookie
        if '@' in node_name:
            self.node_name = node_name
        else:
            self.node_name = '{}@{}'.format(node_name, socket.gethostname())

    def connect(self):
        host_name = socket.gethostname()
        try:
            self.socket = socket.create_connection((host_name,
                                                    self.port))
            self._connected = True
        except socket.error as exc:
            self.logger.error('Could not connect to %s, because of %s',
                              (host_name, self.port, exc))
        self.logger.error('Connected to %s', (host_name,
                                              self.port))

    def send_name(self):
        self.socket.send(encode_name(self.node_name))

    def recv_status(self):
        return decode_status(self.socket)

    def recv_challenge(self):
        return decode_challenge(self.socket)
