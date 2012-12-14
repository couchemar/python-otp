# coding: utf-8
import socket

from gevent import event
from gevent.queue import Queue

from epmd import EPMDKeepAliveConnection, port2_please

from node.connection import OutgoingNodeConnection, Channel
from protocol.node import gen_challenge

from ext import ext_types

from tests import _BaseErlangTestCase


class ChannelTestCase(_BaseErlangTestCase):
    def test_handshake(self):
        conn = EPMDKeepAliveConnection('test', 9999)
        conn.start()

        res = port2_please(self.erl_node_name)
        erl_port = res[1]

        channel = Channel(None)
        channel.connect(erl_port)

        node_name = self.erl_node_name + '@' + socket.gethostname()
        channel.send_name(node_name)
        self.assertEqual(channel.recv_status(), ('s', 'ok'))

        res = channel.recv_challenge()
        self.assertEqual(len(res), 5)
        self.assertEqual(res[0], 'n')

        self.assertEqual(res[4], node_name)

        out_challenge = res[3]
        challenge = gen_challenge()

        channel.send_challenge_reply(self.erl_node_secret,
                                     challenge, out_challenge)
        res = channel.recv_challenge_ack()
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0], 'a')


class OutgoingNodeConnectionTestCase(_BaseErlangTestCase):

    def setUp(self):
        super(OutgoingNodeConnectionTestCase, self).setUp()

        res = port2_please(self.erl_node_name)
        erl_port = res[1]

        connected_event = event.Event()

        res_queue = Queue()

        class _Mock(OutgoingNodeConnection):

            def _process_message(self, message):
                res_queue.put(message)

        self.res_queue = res_queue
        self.connection = _Mock.start('test', erl_port,
                                      self.erl_node_secret,
                                      connected_event)
        connected_event.wait()

        self.node_name = 'test@' + socket.gethostname()

    def test_recv_small_integer(self):
        self.send_message("'_'", self.node_name, '9')

        result = self.res_queue.get()['message'][-1]
        self.assertEqual(result, 9)

    def test_recv_integer(self):
        self.send_message("'_'", self.node_name, '9876')

        result = self.res_queue.get()['message'][-1]
        self.assertEqual(result, 9876)

        self.send_message("'_'", self.node_name, '-9')

        result = self.res_queue.get()['message'][-1]
        self.assertEqual(result, -9)

    def test_recv_float(self):
        self.send_message("'_'", self.node_name, '99.9876')

        result = self.res_queue.get()['message'][-1]
        self.assertEqual(result, 99.9876)

        self.send_message("'_'", self.node_name, '-0.00230022')

        result = self.res_queue.get()['message'][-1]
        self.assertEqual(result, -0.00230022)

    def test_recv_atom(self):
        self.send_message("'_'", self.node_name, 'atom')

        result = self.res_queue.get()['message'][-1]
        self.assertIsInstance(result, ext_types.Atom)
        self.assertEqual(result, 'atom')
