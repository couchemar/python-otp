# coding: utf-8
from epmd import EPMDKeepAliveConnection

conn = EPMDKeepAliveConnection('test@test', 9999)
conn.start()
conn.join()
