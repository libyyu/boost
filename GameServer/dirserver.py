# -*- coding: utf-8 -*-
from tornado import ioloop
from dirinfo.dirsession import DirSession
from network.server import TCPBaseServer
from utils.logger import logger
from utils.singleton import singleton

@singleton
class app(object):
    '''
    class app
    '''
    def __init__(self):
        self.network = TCPBaseServer(delegate=DirSession())

    def stop(self):
        self.network.stop()
        ioloop.IOLoop.instance().stop()

    def run(self, port):
        logger().i("dir server runing at %d", port)
        self.network.run(port)
        ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    try:
        app().run(8002)
    except:
        app().stop()
        quit()