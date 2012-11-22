# coding: utf-8
import struct

def _decode_byte(data):
    [b] = struct.unpack('!B', data[:1])
    return b, data[1:]

def _decode_int(data):
    [i] = struct.unpack('!I', data[:4])
    return i, data[4:]

SMALL_INTEGER_EXT = 97
def decode_small_integer_ext(data):
    return _decode_byte(data)

ATOM_EXT = 100
def decode_atom_ext(data):
    [atom_len] = struct.unpack('!H', data[:2])
    _data = data[2:2+atom_len]
    [atom_name] = struct.unpack('!{}s'.format(atom_len), _data)
    return atom_name, data[2+atom_len:]

PID_EXT = 103
def decode_pid_ext(data):
    # NODE | ID | SERIAL | CREATION
    # NODE:= [ATOM_EXT, SMALL_ATOM_EXT, ATOM_CACHE_REF]
    node, rest = decode_ext(data)
    node_id, rest = _decode_int(rest)
    node_serial, rest = _decode_int(rest)
    node_creation, rest = _decode_byte(rest)
    return (node, node_id, node_serial, node_creation), rest

SMALL_TUPLE_EXT = 104
def decode_small_tuple_ext(data):
    arity, rest = _decode_byte(data)
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
    ext_type, rest = _decode_byte(data)
    return DECODERS[ext_type](rest)


DECODERS = {SMALL_INTEGER_EXT: decode_small_integer_ext,
            ATOM_EXT: decode_atom_ext,
            PID_EXT: decode_pid_ext,
            SMALL_TUPLE_EXT: decode_small_tuple_ext,}
