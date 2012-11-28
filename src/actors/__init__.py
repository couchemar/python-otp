# coding: utf-8
import logging
from pykka.gevent import GeventActor


class BaseActor(GeventActor):
    logger = logging.getLogger('otp.actor')

    def __init__(self):
        super(BaseActor, self).__init__()

    def on_start(self):
        self.logger.info('Starting')
        self._on_start()
        self.logger.info('Started')

    def on_stop(self):
        self.logger.info('Stoping')
        self._on_start()
        self.logger.info('Stoped')

    def on_failure(self, exception_type, exception_value, traceback):
        self.logger.critical('Got exception %s, %s, (Traceback: %s)',
                             exception_type, exception_value, traceback)

    def on_receive(self, message):
        self.logger.info('Received: %s', message)
        self._process_message(message)

    def _on_start(self):
        pass

    def _on_stop(self):
        pass

    def _process_message(self, message):
        pass
