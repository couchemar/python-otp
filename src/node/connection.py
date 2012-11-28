# coding: utf-8
import sys
import logging
from gevent import socket, Greenlet, sleep

import ext
from common.protocol import (encode_message, _decode_message_length,
                             decode_dist_message)
from node.protocol import (encode_name, decode_status, decode_challenge,
                           gen_challenge, gen_digest, encode_challenge_reply,
                           decode_challenge_ack)


class OutgoingNodeConnection(Greenlet):
    logger = logging.getLogger('otp.node.connection')

    encode = lambda self, message: encode_message(message)

    _TIC = sys.float_info.min

    def __init__(self, node_name, port, cookie,
                 in_queue, out_queue):
        super(OutgoingNodeConnection, self).__init__()
        self.port = port
        self.cookie = cookie
        self.state = None
        if '@' in node_name:
            self.node_name = node_name
        else:
            self.node_name = '{}@{}'.format(node_name, socket.gethostname())
        self.in_queue = in_queue
        self.out_queue = out_queue

    def connect(self):
        host_name = socket.gethostname()
        try:
            self.socket = socket.create_connection((host_name,
                                                    self.port))
        except socket.error as exc:
            self.logger.error('Could not connect to %s, because of %s',
                              (host_name, self.port, exc))
            return False
        self.logger.info('Connected to %s', (host_name,
                                             self.port))
        return True

    def _send(self, message):
        self.socket.send(self.encode(message))

    def send_name(self):
        self.logger.info('Sending name')
        self._send(encode_name(self.node_name))
        self.logger.info('Name sended')

    def recv_status(self):
        self.logger.info('Receiving status')
        status = decode_status(self.socket)
        self.logger.info('Status received: %s', status)
        return status

    def recv_challenge(self):
        self.logger.info('Receiving challenge')
        challenge = decode_challenge(self.socket)
        self.logger.info('Challenge received: %s', challenge)
        return challenge

    def send_challenge_reply(self, out_challenge):
        self.logger.info('Sending challenge reply')
        self.challenge = gen_challenge()
        digest = gen_digest(out_challenge, self.cookie)
        self._send(encode_challenge_reply(self.challenge, digest))
        self.logger.info('Challenge reply sended')

    def recv_challenge_ack(self):
        self.logger.info('Receiving challenge ack')
        challenge_ack = decode_challenge_ack(self.socket)
        self.logger.info('Challenge ack received: %s', challenge_ack)
        return challenge_ack

    def do_handshake(self, connected_event):
        self.send_name()
        _, status = self.recv_status()
        if status == 'ok':
            self.logger.info('Status is "ok"')
        else:
            self.logger.warning('Status is "%s" does not know '
                                'what to do with it', status)
            return
        challenge = self.recv_challenge()
        out_challenge = challenge[3]
        self.send_challenge_reply(out_challenge)
        challenge_ack = self.recv_challenge_ack()

        if challenge_ack[1] == gen_digest(self.challenge, self.cookie):
            self.logger.info('Connection is up')
            self.state = 'connected'
            connected_event.set()
        else:
            self.logger.warning('Cannot set up connection, '
                                'because of digest missmatch.')

    def _receive(self, _bytes=4):
        self.logger.debug('Receiving %s bytes', _bytes)
        return self.socket.recv(_bytes)

    def _run(self):
        while 1:
            msg = self._receive()
            if msg == '\x00' * 4:
                self.logger.info('Got ping')
                self._send('')
            else:
                [msg_len] = _decode_message_length(msg, '!I')
                self.logger.info('Received message')
                msg = self._receive(msg_len)
                msg_type, msg_body = decode_dist_message(msg)
                if msg_type != 112:
                    self.logger.error(
                        'Got unexpected message type: %s', msg_type
                    )
                dist_msg = ext.decode(msg_body)
                self.out_queue.put(dist_msg)
            sleep(self._TIC)
