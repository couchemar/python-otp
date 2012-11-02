# coding: utf-8
import unittest
import socket

from epmd import EPMDKeepAliveConnection, port2_please
from node import OutgoingNodeConnection


class NodeTestCase(unittest.TestCase):

    def setUp(self):
        self.erl_node_name = 'erl1'

    def test(self):
        conn = EPMDKeepAliveConnection('test', 9999)
        conn.start()
        res = port2_please(self.erl_node_name)

        erl_port = res[1]

        out_conn = OutgoingNodeConnection('test', erl_port, 'secret')
        out_conn.connect()
        out_conn.send_name()
        self.assertEqual(out_conn.recv_status(), ('s', 'ok'))
        res = out_conn.recv_challenge()
        self.assertEqual(len(res), 5)
        self.assertEqual(res[0], 'n')
        expected_node_name = self.erl_node_name + '@' + socket.gethostname()
        self.assertEqual(res[4], expected_node_name)
        out_conn.send_challenge_reply()
        res = out_conn.recv_challenge_ack()
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0], 'a')
