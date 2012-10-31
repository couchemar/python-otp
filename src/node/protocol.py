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

distrVersion = 5
distrFlags = (DISTR_FLAG_EXTENDEDREFERENCES |
              DISTR_FLAG_EXTENDEDPIDSPORTS |
              DISTR_FLAG_DISTMONITOR)


def _encode_name(node_name, version, flags):
    v_f = struct.pack('!HI', version, flags)
    return 'n{}{}'.format(v_f, node_name)


def encode_name(node_name, version=distrVersion, flags=distrFlags):
    return encode_request(_encode_name(node_name, version, flags))


def decode_status(sock):
    [status_len] = struct.unpack('!H', sock.recv(2))
    status = struct.unpack('!1s{}s'.format(status_len-1),
                           sock.recv(status_len))
    return status
