# -*- coding: utf-8 -*-
import struct
from google.protobuf import descriptor_pb2
try:
    descriptor_pb2.FixRegisterMessageSourceCodeInfo()
    descriptor_pb2.FixRegisterMessageGeneratedCodeInfo()
except Exception as e:
    pass
from protobuf import message_common_pb2
from protobuf import message_client_pb2
from protobuf import message_server_pb2

from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()

_messages = _sym_db.GetMessages(['message_common.proto', 'message_client.proto', 'message_server.proto'])


_id_2_message = {}
_name_2_message = {}
for (full_name, message) in _messages.items():
    if len(message.DESCRIPTOR.fields) >0:
        message_field = message.DESCRIPTOR.fields[0]
        if message_field.name != 'type': continue
        if message_field.enum_type is None: continue
        if message_field.enum_type.name != 'NET_TYPE': continue
        id = message_field.default_value
        _id_2_message[id] = message
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
    try:
        basemsg = message_common_pb2.Message()
        basemsg.ParseFromString(data)
        cls = _id_2_message[basemsg.message_type]
        msg = cls()
        msg.ParseFromString(basemsg.message_body)
        return msg
    except Exception as e:
        pass

def MessageToSendBytes(message):
    meta = message_common_pb2.Message()
    meta.message_type = message.type
    meta.message_body = message.SerializeToString()
    body = meta.SerializeToString()
    bodylen = len(body)
    header = struct.pack('<H', bodylen)
    return header+body

