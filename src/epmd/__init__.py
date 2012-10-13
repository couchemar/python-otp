# coding: utf-8
import struct
import logging
from gevent import Greenlet
from gevent import socket

import codecs

EPMD_HOST = 'localhost'
EPMD_PORT = 4369


class _EPMDConnection(Greenlet):
    logger = logging.getLogger('otp._epmd_connection')
    def __init__(self, epmd_host=EPMD_HOST,
                 epmd_port=EPMD_PORT):
        super(_EPMDConnection, self).__init__()
        self.epmd_host = epmd_host
        self.epmd_port = epmd_port

        self.logger.info('Connect to (%s, %s)', self.epmd_host, self.epmd_port)
        self.socket = socket.create_connection((self.epmd_host,
                                                self.epmd_port))

    def send_request(self, request):
        epmd_request = codecs.encode_request(request)
        self.logger.info('Send request')
        self.socket.send(epmd_request)

    def recv_response(self):
        [resp_code] = struct.unpack('!B', self.socket.recv(1))
        self.logger.info('Receive %s', (resp_code,
                                        codecs.RESPONSES[resp_code]))
        return codecs.decoders[resp_code](self.socket)


class EPMDConnection(_EPMDConnection):
    logger = logging.getLogger('otp.epmd_connection')
    def __init__(self, node_name, port,
                 epmd_host=EPMD_HOST,
                 epmd_port=EPMD_PORT):
        super(EPMDConnection, self).__init__(epmd_host, epmd_port)
        self.node_name = node_name
        self.port = port
        self._status = None
        self._connected = False

    def _register(self):
        self.logger.info('Try to register node. Send %s', codecs.ALIVE2_REQ)
        self._status = 'registering'
        self.send_request(codecs.encode_alive2_req(self.port,
                                                   self.node_name))
        result, creation = self.recv_response()
        self.logger.debug('Registration result: %s', (result, creation))
        if result == 0:
            self.logger.info('Node "%s" with port %s registered',
                             self.node_name, self.port)
            self._status = 'registered'
            self._connected = True
        else:
            self.logger.error('Could not register node')

    def _run(self):
        self._register()
        while self._connected:
            pass


logging.getLogger('otp').setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
