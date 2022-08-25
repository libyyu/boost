# -*- coding: utf-8 -*-
from pio.marshal import Marshal, MarshalException
from pio.octetsstream import OctetsStream
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
		if not iss.eos():
			iss.unmarshalos(os)
		if ptype not in all_protocols:
			logger().w("protocol:%d not register", ptype)
			return None
		protocol = all_protocols[ptype]()
		os.unmarshal(protocol)
		return protocol

	def process(self):
		assert 0, 'abstract method Protocol::process'

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
			logger().e("PBProtocol.marshal wrong:%s", str(e))
		finally:
			return osstream

	def unmarshal(self, isstream):
		try:
			self.message = pb_helper.BytesToMessage(str(isstream))
		except Exception as e:
			logger().e("PBProtocol.unmarshal wrong:%s", str(e))
		finally:
			return isstream

registerProtocol(PBProtocol)