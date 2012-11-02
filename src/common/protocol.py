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
