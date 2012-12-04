# coding: utf-8
import struct
from protocol import encode_message

# EPMD Requests
ALIVE2_REQ_CODE = 120
ALIVE2_REQ = 'ALIVE2_REQ'

ALIVE_CLOSE_REQ = 'ALIVE_CLOSE_REQ'

PORT_PLEASE2_REQ_CODE = 122
PORT_PLEASE2_REQ = 'PORT_PLEASE2_REQ'

NAMES_REQ = 'NAMES_REQ'
DUMP_REQ = 'DUMP_REQ'
KILL_REQ = 'KILL_REQ'
STOP_REQ = 'STOP_REQ'

# EPMD Responses
ALIVE2_RESP_CODE = 121
ALIVE2_RESP = 'ALIVE2_RESP'

PORT2_RESP_CODE = 119
PORT2_RESP = 'PORT2_RESP'
NAMES_RESP = 'NAMES_RESP'
DUMP_RESP = 'DUMP_RESP'
KILL_RESP = 'KILL_RESP'
STOP_OK_RESP = 'STOP_OK_RESP'
STOP_NOTOK_RESP = 'STOP_NOTOK_RESP'

RESPONSES = {ALIVE2_RESP_CODE: ALIVE2_RESP,
             PORT2_RESP_CODE: PORT2_RESP}


def encode_request(request):
    """
    Each request *_REQ is preceded by a two-byte length field.
    """
    return encode_message(request)


def encode_alive2_req(port, node_name, extra="",
                      node_type=72, protocol=0,
                      highest_version=5,
                      lowest_version=5):
    """
    Register node in the EPMD
    """
    r_format = (
        '!B'  # code
        'H'  # port
        'B'  # node type
        'B'  # protocol
        'H'  # highest version
        'H'  # lowest version
        'H'  # Node name length
        '{node_name_length}s'  # Node Name
        'H'  # Extra length
        '{extra_length}s'  # extra
    )
    req_code = ALIVE2_REQ_CODE
    node_name_length = len(node_name)
    extra_length = len(extra)
    r_format = r_format.format(node_name_length=node_name_length,
                               extra_length=extra_length)
    return struct.pack(r_format, req_code, port, node_type, protocol,
                       highest_version, lowest_version, node_name_length,
                       node_name, extra_length, extra)


def encode_port_please2_req(node_name):
    r_format = '!B{}s'.format(len(node_name))
    req_code = PORT_PLEASE2_REQ_CODE
    return struct.pack(r_format, req_code, node_name)


def decode_alive2_resp(sock):
    return struct.unpack('!BH', sock.recv(3))


def decode_port_please2_resp(sock):
    [result] = struct.unpack('!B', sock.recv(1))
    if result > 0:
        return result
    else:
        fmt = '!HBBHHH'
        (port, node_type,
         protocol, hv,
         lv, nlen) = struct.unpack(fmt, sock.recv(struct.calcsize(fmt)))
        [node_name] = struct.unpack('!{}s'.format(nlen), sock.recv(nlen))
        [elen] = struct.unpack('!H', sock.recv(2))
        [extra] = struct.unpack('!{}s'.format(elen), sock.recv(elen))
    return (result, port, node_type, protocol, hv, lv,
            nlen, node_name, elen, extra)

decoders = {ALIVE2_RESP_CODE: decode_alive2_resp,
            PORT2_RESP_CODE: decode_port_please2_resp}
