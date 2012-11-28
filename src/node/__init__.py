# coding: utf-8
import sys
import logging
from gevent import Greenlet, sleep, event
from gevent.queue import Queue

import epmd

from node.connection import OutgoingNodeConnection


class Node(Greenlet):
    logger = logging.getLogger('otp.node')

    CONNECT_NODE_TIMEOUT = 5
    _TIC = sys.float_info.min

    def __init__(self, node_name, cookie,
                 listening_port, in_queue=None, out_queue=None):
        super(Node, self).__init__()
        self.node_name = node_name
        self.cookie = cookie
        self.listening_port = listening_port

        self.epmd_connection = epmd.EPMDKeepAliveConnection(
            node_name, listening_port
        )

        self.node_connections = {}
        if in_queue is None:
            self.in_queue = Queue()
        else:
            self.in_queue = in_queue
        if out_queue is None:
            self.out_queue = Queue()
        else:
            self.out_queue = out_queue

    def _run(self):
        self.epmd_connection.start()
        while 1:
            sleep(self._TIC)

    def connect_node(self, out_node_name):
        res = epmd.port2_please(out_node_name)
        out_port = res[1]

        if out_node_name in self.node_connections:
            self.logger.warning('Already connected to "%s"', out_node_name)
        else:
            connected_event = event.Event()
            out_conn = OutgoingNodeConnection(
                self.node_name,
                out_port,
                self.cookie,
                in_queue=self.out_queue,
                out_queue=self.in_queue)
            if out_conn.connect():
                out_conn.do_handshake(connected_event)

            if connected_event.wait(self.CONNECT_NODE_TIMEOUT):
                self.node_connections[out_node_name] = out_conn
                out_conn.start()
            else:
                self.logger.warning('Does not connected to "%s:%s" '
                                    'after %s seconds',
                                    out_node_name, out_port,
                                    self.CONNECT_NODE_TIMEOUT)
