# -*- coding: utf-8 -*-
import os

from network.server import TCPConnectionDelegage
from utils.logger import logger
from protobuf import pb_helper
from pio.octetsstream import OctetsStream
from pio.protocol import Protocol, PBProtocol
from protobuf import message_common_pb2

class DirSession(TCPConnectionDelegage):
    def __init__(self):
        TCPConnectionDelegage.__init__(self)

    def on_connect(self):
        logger().i("%s client connected.", str(self.address))
        pass

    def on_receive(self, data):
        logger().i("receive from %s %d", str(self.address), len(data))
        
        try:
            oss = OctetsStream(order='!').replace(data)
            protocol = Protocol.decode(oss)
            if protocol: protocol.process()
        except Exception as e:
            logger().e("PBProtocol.marshal wrong:%s", str(e))
                

    def SendProtocol(self, protocol):
        oss = OctetsStream(order='!')
        protocol.encode(oss)

        buffer = OctetsStream(order='!')
        buffer.marshal_uint16(len(oss))
        buffer.append(oss)

        logger().i("send protocol(%s) to %s, len:%d", str(protocol), str(self.address), len(buffer))
        self.send(str(buffer))

    def _send_dirinfo(self):
        logger().i("_send_dirinfo")
        path = os.path.split(os.path.realpath(__file__))[0].replace("\\", "/")
        msg = message_common_pb2.DirInfo()
        filename = path + "/bin/version.xml"
        with open(filename,"rb") as fin:
            data = fin.read()
            msg.version = data
            fin.close()
        filename = path + "/bin/version.txt"
        with open(filename, "rb") as fin:
            data = fin.read()
            msg.patches = data
            fin.close()

        protocol = PBProtocol()
        protocol.message = msg

        self.SendProtocol(protocol)
            

    def on_write_complete(self):
        #self.close()
        pass