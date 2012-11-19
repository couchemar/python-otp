# coding: utf-8
import struct


def decode_small_tuple_ext(data):
    arity = struct.unpack('!B', data[0])
    elements_data = data[1:]
    decode_ext(elements_data)


def decode(data):
    [ext_type] = struct.unpack('!B', data[0])
    return decode_ext(data[1:])

def decode_ext(data):
    [ext_type] = struct.unpack('!B', data[0])
    return DECODERS[ext_type](data[1:])

SMALL_TUPLE_EXT = 104
DECODERS = {SMALL_TUPLE_EXT: decode_small_tuple_ext}
