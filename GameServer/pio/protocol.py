# -*- coding: utf-8 -*-
from marshal import Marshal, MarshalException
from octetsstream import OctetsStream
from protobuf import pb_helper

all_protocols = {}

def registerProtocol(cls):
	all_protocols[cls.protocol()] = cls

class Protocol(Marshal):
	'''
	Protocol
	'''
	

	def __init__(self):
		pass

	def encode(self, os):
		os.marshal_uint16(self.protocol())
		os.marshalos(OctetsStream().marshal(self))

	@classmethod
	def decode(cls, iss):
		ptype = iss.unmarshal_uint16()
		os = OctetsStream()
		iss.unmarshal(os)
		protocol = all_protocols[ptype]()
		os.unmarshal(protocol)
		return protocol



class PBProtocol(Protocol):
	def __init__(self):
		self.message = None

	@classmethod
	def protocol(cls):
		return 1

	def marshal(self, osstream):
		buffer = pb_helper.MessageToSendBytes(self.message)
		osstream.append(buffer)

	def unmarshal(self, isstream):
		buffer = isstream.getbytes()
		self.message = pb_helper.BytesToMessage(buffer)



registerProtocol(PBProtocol)