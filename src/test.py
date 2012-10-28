# coding: utf-8
from epmd import EPMDKeepAliveConnection, port2_please

conn = EPMDKeepAliveConnection('test', 9999)
conn.start()

print port2_please('erl1')

conn.join(1)
