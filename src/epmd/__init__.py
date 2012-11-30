# coding: utf-8
import sys
import struct
import logging
from gevent import sleep, socket, Greenlet

from epmd import codecs

EPMD_HOST = 'localhost'
EPMD_PORT = 4369


class EPMDConnection(Greenlet):
    logger = logging.getLogger('otp.epmd_connection')

    _TIC = sys.float_info.min

    def __init__(self, epmd_host=None,
                 epmd_port=None):
        super(EPMDConnection, self).__init__()
        self._connected = False
        if epmd_host is not None:
            self.epmd_host = epmd_host
        else:
            self.epmd_host = EPMD_HOST
        if epmd_port is not None:
            self.epmd_port = epmd_port
        else:
            self.epmd_port = EPMD_PORT

        self.logger.info('Connect to (%s, %s)',
                         self.epmd_host, self.epmd_port)

        try:
            self.socket = socket.create_connection((self.epmd_host,
                                                    self.epmd_port))
            self._connected = True
        except socket.error as exc:
            self.logger.error('Could not connect to %s because of %s',
                              (self.epmd_host,
                               self.epmd_port,
                               exc))

    def send_request(self, request):
        epmd_request = codecs.encode_request(request)
        self.logger.info('Send request')
        self.socket.send(epmd_request)

    def recv_response(self):
        self.logger.info('Receive')
        [resp_code] = struct.unpack('!B', self.socket.recv(1))
        self.logger.info('Received: %s', (resp_code,
                                          codecs.RESPONSES[resp_code]))
        return codecs.decoders[resp_code](self.socket)


class EPMDKeepAliveConnection(EPMDConnection):
    logger = logging.getLogger('otp.epmd_keep_alive_connection')

    def __init__(self, node_name, port,
                 epmd_host=None,
                 epmd_port=None):
        super(EPMDKeepAliveConnection, self).__init__(epmd_host, epmd_port)
        self.node_name = node_name
        self.port = port
        self._status = None

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
        if not self._connected:
            return
        self._register()
        while self._connected and self._status == 'registered':
            sleep(self._TIC)


def port2_please(node_name, host=None, port=None):
    node_name = node_name.split('@')[0]
    conn = EPMDConnection(host, port)
    conn.send_request(codecs.encode_port_please2_req(node_name))
    return conn.recv_response()


logging.getLogger('otp').setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
