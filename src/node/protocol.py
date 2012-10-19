# coding: utf-8
import struct
from epmd.codecs import encode_request

 DISTR_FLAG_PUBLISHED = 1
 DISTR_FLAG_ATOMCACHE = 2
 DISTR_FLAG_EXTENDEDREFERENCES = 4
 DISTR_FLAG_DISTMONITOR = 8
 DISTR_FLAG_FUNTAGS = 16
 DISTR_FLAG_DISTMONITORNAME = 32
 DISTR_FLAG_HIDDENATOMCACHE = 64
 DISTR_FLAG_NEWFUNTAGS = 128
 DISTR_FLAG_EXTENDEDPIDSPORTS = 256


def encode_name(version, flags, node_name):
    v_f = struct.pack('!HI', version, flags)
    return "n{}{}".format(v_f, node_name)

