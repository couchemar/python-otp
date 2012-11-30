# coding: utf-8
import logging
from gevent import event

import epmd

from actors import BaseActor

from node.connection import OutgoingNodeConnection


class Node(BaseActor):
    logger = logging.getLogger('otp.node')

    CONNECT_NODE_TIMEOUT = 5

    def __init__(self, node_name, cookie,
                 listening_port):
        super(Node, self).__init__()
        self.node_name = node_name
        self.cookie = cookie
        self.listening_port = listening_port

        self.epmd_connection = epmd.EPMDKeepAliveConnection(
            node_name, listening_port
        )

        self.node_connections = {}

    def _on_start(self):
        self.epmd_connection.start()

    def connect_node(self, out_node_name):
        res = epmd.port2_please(out_node_name)
        out_port = res[1]

        if out_node_name in self.node_connections:
            self.logger.warning('Already connected to "%s"', out_node_name)
        else:
            connected_event = event.Event()
            out_conn = OutgoingNodeConnection.start(
                self.node_name,
                out_port,
                self.cookie,
                connected_event
            )

            if connected_event.wait(self.CONNECT_NODE_TIMEOUT):
                self.node_connections[out_node_name] = out_conn
                return True
            else:
                self.logger.warning('Does not connected to "%s:%s" '
                                    'after %s seconds',
                                    out_node_name, out_port,
                                    self.CONNECT_NODE_TIMEOUT)
                return False
