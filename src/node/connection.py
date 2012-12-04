# coding: utf-8
import sys
import logging
from gevent import socket, Greenlet, sleep

import ext
from protocol import (encode_message, _decode_message_length,
                      decode_dist_message)
from protocol.node import (encode_name, decode_status,
                           decode_challenge, gen_challenge,
                           gen_digest, encode_challenge_reply,
                           decode_challenge_ack)

from actors import BaseActor


class Channel(Greenlet):
    logger = logging.getLogger('otp.node.connection.channel')

    encode = lambda self, message: encode_message(message)

    _TIC = sys.float_info.min

    def __init__(self, ref):
        super(Channel, self).__init__()
        self.ref = ref
        self.socket = None

    def connect(self, port):
        host_name = socket.gethostname()
        try:
            self.socket = socket.create_connection((host_name, port))
        except socket.error as exc:
            self.logger.error('Could not connect to %s, because of %s',
                              (host_name, port, exc))
            return False
        self.logger.info('Connected to %s', (host_name, port))
        return True

    def _send(self, message):
        self.socket.send(self.encode(message))

    def send_name(self, node_name):
        self.logger.info('Sending name')
        self._send(encode_name(node_name))
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

    def send_challenge_reply(self, cookie, challenge, out_challenge):
        self.logger.info('Sending challenge reply')
        digest = gen_digest(out_challenge, cookie)
        self._send(encode_challenge_reply(challenge, digest))
        self.logger.info('Challenge reply sended')

    def recv_challenge_ack(self):
        self.logger.info('Receiving challenge ack')
        challenge_ack = decode_challenge_ack(self.socket)
        self.logger.info('Challenge ack received: %s', challenge_ack)
        return challenge_ack

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
                self.ref.tell({'message': dist_msg})
            sleep(self._TIC)


class OutgoingNodeConnection(BaseActor):
    logger = logging.getLogger('otp.node.connection')

    def __init__(self, node_name, port, cookie, connected_event=None):
        super(OutgoingNodeConnection, self).__init__()
        self.port = port
        self.cookie = cookie
        if '@' in node_name:
            self.node_name = node_name
        else:
            self.node_name = '{}@{}'.format(node_name, socket.gethostname())

        self.channel = Channel(self.actor_ref)
        self.channel.connect(self.port)
        self.connected_event = connected_event
        self._state = None

    def _get_state(self):
        return self._state

    @property
    def state(self):
        return self._get_state()

    def do_handshake(self):
        self.logger.info('Do handshake')
        self.channel.send_name(self.node_name)
        _, status = self.channel.recv_status()
        if status == 'ok':
            self.logger.info('Status is "ok"')
        else:
            self.logger.warning('Status is "%s" does not know '
                                'what to do with it', status)
            return
        challenge = self.channel.recv_challenge()
        out_challenge = challenge[3]
        challenge = gen_challenge()
        self.channel.send_challenge_reply(self.cookie, challenge,
                                          out_challenge)
        challenge_ack = self.channel.recv_challenge_ack()
        if challenge_ack[1] == gen_digest(challenge, self.cookie):
            self.logger.info('Connection is up')
            self._state = 'connected'
            if self.connected_event is not None:
                self.connected_event.set()
        else:
            self.logger.warning('Cannot set up connection, '
                                'because of digest missmatch.')

    def _on_start(self):
        self.do_handshake()
        self.channel.start()
