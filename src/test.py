# coding: utf-8
from epmd import EPMDConnection
from epmd.codecs import encode_alive2_req

conn = EPMDConnection('test@test', 9999)
conn.start()
conn.join()
