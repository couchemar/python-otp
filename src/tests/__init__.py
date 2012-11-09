# coding: utf-8
import os
import subprocess

import time
import unittest

class _BaseErlangTestCase(unittest.TestCase):

    def setUp(self):
        self.erl_node_name = 'erl1'
        self.erl_node_secret = 'secret'

        _dir = os.path.dirname(__file__)
        _pth = os.path.join(_dir, 'test.sh')
        self.erl = subprocess.Popen(
            ['erl', '-noinput',
             '-sname', self.erl_node_name,
             '-setcookie', self.erl_node_secret]
        )
        time.sleep(0.4)

    def tearDown(self):
        self.erl.kill()
