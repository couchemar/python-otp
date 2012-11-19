# coding: utf-8
import struct


def decode_small_integer_ext(data):
    return struct.unpack('!B', data[0]), data[1:]

def decode_small_tuple_ext(data):
    arity = struct.unpack('!B', data[0])
    rest = data[1:]
    e = 0
    _t = []
    while e < arity:
        el, rest = decode_ext(rest)
        _t.append(el)
        e += 1
    return tuple(_t), rest

def decode(data):
    [ext_type] = struct.unpack('!B', data[0])
    return decode_ext(data[1:])

def decode_ext(data):
    [ext_type] = struct.unpack('!B', data[0])
    return DECODERS[ext_type](data[1:])


SMALL_INTEGER_EXT = 97
SMALL_TUPLE_EXT = 104

DECODERS = {SMALL_INTEGER_EXT: decode_small_integer_ext,
            SMALL_TUPLE_EXT: decode_small_tuple_ext}
