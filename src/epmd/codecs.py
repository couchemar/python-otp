# coding: utf-8
import struct

# EPMD Requests
ALIVE2_REQ = 'ALIVE2_REQ'
ALIVE_CLOSE_REQ = 'ALIVE_CLOSE_REQ'
PORT_PLEASE2_REQ = 'PORT_PLEASE2_REQ'
NAMES_REQ = 'NAMES_REQ'
DUMP_REQ = 'DUMP_REQ'
KILL_REQ = 'KILL_REQ'
STOP_REQ = 'STOP_REQ'

# EPMD Responses
ALIVE2_RESP = 'ALIVE2_RESP'
PORT2_RESP = 'PORT2_RESP'
NAMES_RESP = 'NAMES_RESP'
DUMP_RESP = 'DUMP_RESP'
KILL_RESP = 'KILL_RESP'
STOP_OK_RESP = 'STOP_OK_RESP'
STOP_NOTOK_RESP = 'STOP_NOTOK_RESP'


def encode_request(request):
    """
    Each request *_REQ is preceded by a two-byte length field.
    """
    request_len = len(request)
    return struct.pack('!H{}s'.format(request_len),
                       request_len, request)


def encode_alive2_req(port, node_name, extra="",
                      node_type=72, protocol=0,
                      highest_version=5,
                      lowest_version=5):
    """
    Register node in the EPMD
    """
    r_format = (
        '!B' # code
        'H' # port
        'B' # node type
        'B' # protocol
        'H' # highest version
        'H' # lowest version
        'H' # Node name length
        '{node_name_length}s' # Node Name
        'H' # Extra length
        '{extra_length}s' # extra
    )
    req_code = 120
    node_name_length = len(node_name)
    extra_length = len(extra)
    r_format = r_format.format(node_name_length=node_name_length,
                               extra_length=extra_length)
    return struct.pack(r_format, req_code, port, node_type, protocol,
                       highest_version, lowest_version, node_name_length,
                       node_name, extra_length, extra)


def decode_alive2_resp(sock):
    return struct.unpack('!BH', sock.recv(3))

decoders = {121: decode_alive2_resp}
