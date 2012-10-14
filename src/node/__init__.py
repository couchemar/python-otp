# coding: utf-8
import logging
from gevent import sleep, socket, Greenlet


class OutgoingNodeConnection(Greenlet):
    logger = logging.getLogger('otp.node.connection')

    def __init__(self, port, cookie):
        pass
