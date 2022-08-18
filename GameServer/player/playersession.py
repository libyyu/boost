# -*- coding: utf-8 -*-
import struct

from network.server import TCPConnectionDelegage
from protobuf import message_common_pb2
from protobuf import message_client_pb2
from protobuf import message_server_pb2
from protobuf import pb_helper
from utils.logger import logger


class PlayerSession(TCPConnectionDelegage):
    """
    one client
    """
    def __init__(self):
        TCPConnectionDelegage.__init__(self)

    def on_connect(self):
        logger().i("%s client connected.", str(self.address))
        pass

    def on_timeout(self):
        pass

    def on_receive(self, data):
        logger().i("receive from %s, %s", str(self.address),pb_helper.debug_bytes(data))
        msg = pb_helper.BytesToMessage(data)
        if isinstance(msg, message_client_pb2.TestMessage):
            self.on_login()

    def on_write_complete(self):
        pass

    def on_close(self):
        logger().i("%s client closed.", str(self.address))
        pass

    def on_login(self):
        msg = message_server_pb2.TestMessageRe()
        msg.id = 200
        msg.buff = "welcome!"
        self.SendMessage(msg)

    def SendMessage(self,message):
        buff = pb_helper.MessageToSendBytes(message)
        logger().i("send to %s, %s", str(self.address), pb_helper.debug_bytes(buff))
        self.send(buff)
