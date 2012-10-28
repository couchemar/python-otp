# coding: utf-8
import os
import unittest
import subprocess

from time import sleep

from epmd import EPMDKeepAliveConnection, port2_please


class EPMDTestCase(unittest.TestCase):

    def setUp(self):
        self.erl_node_name = 'erl1'
        _dir = os.path.dirname(__file__)
        _dir = os.path.join(_dir, 'test.sh')
        self.shell = subprocess.Popen(['sh', _dir])
        sleep(0.1)

    def tearDown(self):
        self.shell.terminate()
        self.shell.kill()

    def test(self):
        conn = EPMDKeepAliveConnection('test', 9999)
        conn.start()

        res = port2_please(self.erl_node_name)
        conn.join(0.1)
        self.assertEqual(len(res), 10)
        self.assertEqual(res[7], 'erl1')
