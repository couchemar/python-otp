# coding: utf-8
from epmd import EPMDConnection
from epmd.codecs import encode_alive2_req

conn = EPMDConnection()

conn.send_request(encode_alive2_req(9999, 'test@node'))
print 'Got: ', conn.recv_response()

