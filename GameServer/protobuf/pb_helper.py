# -*- coding: utf-8 -*-
import struct

from protobuf import message_common_pb2
# from protobuf import message_client_pb2
# from protobuf import message_server_pb2

from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()

_messages = _sym_db.GetMessages(['message_common.proto'])


_id_2_message = {}
_name_2_message = {}
for (full_name, message) in _messages.items():
    msg_type = message.DESCRIPTOR.GetOptions().Extensions[message_common_pb2.npt_type]
    if msg_type:
        _id_2_message[msg_type] = message
        _name_2_message[full_name] = message



def import_driver(drivers, preferred=None):
    """Import the first available driver or preferred driver.
    """
    if preferred:
        drivers = [preferred]

    for d in drivers:
        try:
            return __import__(d, None, None, ['x'])
        except ImportError:
            pass
    raise ImportError("Unable to import " + " or ".join(drivers))

def debug_bytes(data):
    tstr = ""
    for i in range(len(data)):
        sep = ',' if i <len(data)-1 else ''
        tstr = tstr + hex(ord(data[i])) + sep
    return tstr

def BytesToMessage(data):
    basemsg = message_common_pb2.Message()
    basemsg.ParseFromString(data)
    if basemsg.message_type not in _id_2_message:
        raise Exception("message_type %d not found."% basemsg.message_type)
    cls = _id_2_message[basemsg.message_type]
    msg = cls()
    msg.ParseFromString(basemsg.message_body)
    return msg

def MessageToSendBytes(message):
    message_type = message.DESCRIPTOR.GetOptions().Extensions[message_common_pb2.npt_type]
    meta = message_common_pb2.Message()
    meta.message_type = message_type
    meta.message_body = message.SerializeToString()
    body = meta.SerializeToString()
    return body

