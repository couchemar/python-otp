# coding: utf-8
import struct


def encode_message(message, fmt=None):
    message_len = len(message)
    if fmt == None:
        fmt='!H'
    return struct.pack('{}{}s'.format(fmt, message_len),
                       message_len, message)


def decode_message_length(sock, fmt=None):
    if fmt == None:
        fmt='!H'
    return struct.unpack(fmt, sock.recv(struct.calcsize(fmt)))


def _decode_message_length(message, fmt=None):
    if fmt == None:
        fmt='!H'
    return struct.unpack(fmt, message)


def decode_dist_message(message):
    return struct.unpack('!B{}s'.format(len(message)-1), message)
