# coding: utf-8
import logging
from gevent import socket, Greenlet
from node.protocol import (encode_name, decode_status, decode_challenge,
                           gen_challenge, gen_digest, encode_challenge_reply,
                           decode_challenge_ack)


class OutgoingNodeConnection(Greenlet):
    logger = logging.getLogger('otp.node.connection')

    def __init__(self, node_name, port, cookie):
        super(OutgoingNodeConnection, self).__init__()
        self.port = port
        self.cookie = cookie
        if '@' in node_name:
            self.node_name = node_name
        else:
            self.node_name = '{}@{}'.format(node_name, socket.gethostname())

    def connect(self):
        host_name = socket.gethostname()
        try:
            self.socket = socket.create_connection((host_name,
                                                    self.port))
            self._connected = True
        except socket.error as exc:
            self.logger.error('Could not connect to %s, because of %s',
                              (host_name, self.port, exc))
            return
        self.logger.info('Connected to %s', (host_name,
                                             self.port))

    def send_name(self):
        self.logger.info('Sending name')
        self.socket.send(encode_name(self.node_name))
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
        self.other_challenge = challenge[3]
        return challenge

    def send_challenge_reply(self):
        self.logger.info('Sending challenge reply')
        self.challenge = gen_challenge()
        digest = gen_digest(self.other_challenge, self.cookie)
        self.socket.send(encode_challenge_reply(self.challenge, digest))
        self.logger.info('Challenge reply sended')

    def recv_challenge_ack(self):
        self.logger.info('Receiving challenge ack')
        challenge_ack = decode_challenge_ack(self.socket)
        self.logger.info('Challenge ack received: %s', challenge_ack)
        return challenge_ack
