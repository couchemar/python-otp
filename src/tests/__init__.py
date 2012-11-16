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

    def exec_function(self, message):
        return subprocess.check_output(
            ['erl_call',
             '-sname', self.erl_node_name,
             '-c', self.erl_node_secret,
             '-h', 'to_erl',
             '-a', message]

        )

    def exec_on_erl(self, message):
        erl = subprocess.Popen(
            ['erl_call',
             '-sname', self.erl_node_name,
             '-c', self.erl_node_secret,
             '-h', 'to_erl',
             '-e'],
             stdin=subprocess.PIPE,
             stdout=subprocess.PIPE,
             stderr=subprocess.PIPE
        )
        out, err = erl.communicate('{}\n'.format(message))
        ret = erl.returncode
        self.assertFalse(err or ret != 0,
                         'Error: {}, returncode: {}'.format(err, ret))
        return out

    def send_message(self, proc, node, message):
        res = self.exec_on_erl(
            '{' + proc + ', ' + node + '} !' + '{}.'.format(message)
        )
        self.assertEqual(res, '{ok, ' +'{}'.format(message) + '}')
        return res
