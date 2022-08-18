# -*- coding: utf-8 -*-
import logging

from utils.singleton import singleton
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10

@singleton
class logger(object):
    """
    logger for logging
    """
    log = logging.getLogger()

    def __init__(self,level=DEBUG,format='%(asctime)s -%(module)s:%(filename)s:%(lineno)d-%(levelname)s: %(message)s'):
        self.setLevel(level)
        self.setFormat(format)
        logging.info("Current log level is : %s", logging.getLevelName(self.log.getEffectiveLevel()))

    def setLevel(self,level):
        assert self.log != None, "logger is not init."
        self.log.setLevel(level)
        return self

    def setFormat(self,format):
        assert self.log != None, "logger is not init."
        sh = logging.StreamHandler()
        formatter = logging.Formatter(format)
        sh.setFormatter(formatter)
        self.log.addHandler(sh)
        return self

    def e(self, msg, *args, **kwargs):
        logging.error(msg, *args, **kwargs)

    def excpt(self, msg, *args, **kwargs):
        logging.exception(msg, *args, **kwargs)

    def w(self, msg, *args, **kwargs):
        logging.warning(msg, *args, **kwargs)

    def i(self, msg, *args, **kwargs):
        logging.info(msg, *args, **kwargs)

    def d(self, msg, *args, **kwargs):
        logging.debug(msg, *args, **kwargs)


if __name__ == "__main__":
    logger(level=DEBUG).d("hello")
    logger().setLevel(INFO).i("hello2")
