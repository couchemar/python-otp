# coding: utf-8
import unittest
import subprocess

from epmd import EPMDKeepAliveConnection, port2_please

class EPMDTestCase(unittest.TestCase):

    def setUp(self):
        self.erl_node_name = 'erl1'
        self.erl = subprocess.Popen(
            ['erl',
             '-noinput',
             '-sname {}'.format(self.erl_node_name)]
        )

    def tearDown(self):
        self.erl.terminate()

    def test(self):
        conn = EPMDKeepAliveConnection('test', 9999)
        conn.start()

        res = port2_please(self.erl_node_name)
        self.assertEqual(res, 0)
        conn.join(1)
