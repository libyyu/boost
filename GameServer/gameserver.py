# -*- coding: utf-8 -*-
import threading

from tornado import ioloop

from network.server import TCPBaseServer
from player.playersession import PlayerSession
from utils.logger import logger
from utils.singleton import singleton


@singleton
class app(object):
    '''
    class app
    '''
    def __init__(self):
        self.network = TCPBaseServer(handle=PlayerSession)

    def stop(self):
        self.network.stop()
        ioloop.IOLoop.instance().stop()

    def run(self, port):
        logger().i("app runing.")
        logger().i("network run at %d", port)
        #t = threading.Thread(target=lambda p:self.network.run(p), args=(port,))
        #t.start()
        self.network.run(port)
        ioloop.IOLoop.instance().start()

def main():
    app().run(8001)

if __name__ == "__main__":
    try:
        main()
    except:
        quit()