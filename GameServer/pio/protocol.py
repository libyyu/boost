# -*- coding: utf-8 -*-
from marshal import Marshal, MarshalException
from octetsstream import OctetsStream
from protobuf import pb_helper
from utils.enum import Enum
from utils.logger import logger

all_protocols = {}
def registerProtocol(cls):
	all_protocols[cls.protocol()] = cls


PROTOCOL_TYPE = Enum("MESSAGE_BEGIN",
               "MESSAGE_TEST",
               "MESSAGE_PB")

EndianMode = Enum("None", "BigEndian", "LittleEndian", "Network")


class Protocol(Marshal):
	'''
	Protocol
	'''
	def encode(self, os):
		os.marshal_uint16(self.protocol())
		os.marshalos(OctetsStream().marshal(self))

	@classmethod
	def decode(cls, iss):
		ptype = iss.unmarshal_uint16()
		os = OctetsStream()
		iss.unmarshalos(os)
		if ptype not in all_protocols:
			return None
		protocol = all_protocols[ptype]()
		os.unmarshal(protocol)
		return protocol

class PBProtocol(Protocol):
	def __init__(self, message = None):
		self.message = message

	@classmethod
	def protocol(cls):
		return PROTOCOL_TYPE.MESSAGE_PB

	def marshal(self, osstream):
		try:
			buffer = pb_helper.MessageToSendBytes(self.message)
			osstream.append(buffer)
		except Exception as e:
			logger.w("PBProtocol.marshal wrong:%s", str(e))
		finally:
			return osstream

	def unmarshal(self, isstream):
		try:
			self.message = pb_helper.BytesToMessage(str(isstream))
		except Exception as e:
			logger.w("PBProtocol.unmarshal wrong:%s", str(e))
		finally:
			return isstream

registerProtocol(PBProtocol)