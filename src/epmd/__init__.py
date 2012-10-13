# coding: utf-8
import struct
import logging
from gevent import Greenlet
from gevent import socket

from codecs import encode_request, encode_alive2_req, decoders

EPMD_HOST = 'localhost'
EPMD_PORT = 4369


class EPMDConnection(Greenlet):
    def __init__(self, epmd_host=EPMD_HOST,
                 epmd_port=EPMD_PORT):
        super(EPMDConnection, self).__init__()
        self.epmd_host = epmd_host
        self.epmd_port = epmd_port

        logging.info('Connect to (%s, %s)', self.epmd_host, self.epmd_port)
        self.socket = socket.create_connection((self.epmd_host,
                                                self.epmd_port))

    def send_request(self, request):
        epmd_request = encode_request(request)
        logging.info('Send request')
        self.socket.send(epmd_request)

    def recv_response(self):
        [resp_code] = struct.unpack('!B', self.socket.recv(1))
        logging.info('Receive %s code', resp_code)
        return decoders[resp_code](self.socket)

logging.basicConfig(level=logging.DEBUG)
