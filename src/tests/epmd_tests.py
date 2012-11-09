# coding: utf-8
import os
import unittest
import subprocess

from time import sleep

from epmd import EPMDKeepAliveConnection, port2_please

from tests import _BaseErlangTestCase

class EPMDTestCase(_BaseErlangTestCase):

    def test(self):
        conn = EPMDKeepAliveConnection('test', 9999)
        conn.start()

        res = port2_please(self.erl_node_name)
        conn.join(0.1)
        self.assertEqual(len(res), 10)
        self.assertEqual(res[7], 'erl1')
