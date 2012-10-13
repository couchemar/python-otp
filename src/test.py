# coding: utf-8
from epmd import EPMDKeepAliveConnection, port2_please

import gevent

conn = EPMDKeepAliveConnection('test@andrey-1215N', 9999)
conn.start()

print port2_please('erl1')

conn.join(1)




