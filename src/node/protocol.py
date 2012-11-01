# coding: utf-8
import struct
import random
import hashlib
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


def _decode_length(sock, fmt=None):
    if fmt == None:
        fmt='!H'
    return struct.unpack(fmt, sock.recv(struct.calcsize(fmt)))


def decode_status(sock):
    [status_len] = _decode_length(sock)
    return struct.unpack('!1s{}s'.format(status_len-1),
                         sock.recv(status_len))



def decode_challenge(sock):
    [ch_len] = _decode_length(sock)
    _fmt = '!sHII'
    name_fmt = '{}s'.format(ch_len - struct.calcsize(_fmt))
    fmt = '{}{}'.format(_fmt, name_fmt)
    return struct.unpack(fmt, sock.recv(ch_len))


def gen_challenge():
    random.seed()
    return int(random.randint(0, 2**32))


def gen_digest(challenge, cookie):
    return hashlib.md5(cookie + str(challenge)).digest()
