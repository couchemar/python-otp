# coding: utf-8
import subprocess

import time
import unittest

class _BaseErlangTestCase(unittest.TestCase):

    def setUp(self):
        self.erl_node_name = 'erl1'
        self.erl_node_secret = 'secret'

        self.erl = subprocess.Popen(
            ['erl', '-noinput',
             '-sname', self.erl_node_name,
             '-setcookie', self.erl_node_secret]
        )
        time.sleep(0.4)

    def tearDown(self):
        self.erl.kill()

    def to_erl(self, message):
        return subprocess.check_output(
            ['erl_call',
             '-sname', self.erl_node_name,
             '-c', self.erl_node_secret,
             '-h', 'to_erl',
             '-a', message]
        )
