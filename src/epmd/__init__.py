# coding: utf-8
import logging
from gevent import Greenlet
from gevent import socket


EPMD_HOST = 'localhost'
EPMD_PORT = 4369


class EPMDConnection(Greenlet):
    def __init__(self, epmd_host=EPMD_HOST,
                 epmd_port=EPMD_PORT):
        super(EPMDConnection, self).__init__()
        self.epmd_host = epmd_host
        self.epmd_port = epmd_port

        self.socket = socket.
