# coding: utf-8
import pykka

from node import Node

from tests import _BaseErlangTestCase


class SimpleNodeTestCase(_BaseErlangTestCase):

    def test(self):
        node = Node('test', self.erl_node_secret, 9999)
        node.start()
        node.connect_node(self.erl_node_name)
        conn_ref = node.node_connections[self.erl_node_name]
        conn = pykka.ActorProxy(conn_ref)
        self.assertEqual(conn.state.get(), 'connected')
        self.assertTrue('test' in self.exec_function('erlang nodes [hidden]'))
        node.join(0.1)
