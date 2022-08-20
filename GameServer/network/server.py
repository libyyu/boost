# -*- coding: utf-8 -*-
import threading
import struct
from tornado import ioloop, gen, iostream
from tornado.tcpserver import TCPServer
from tornado import stack_context
from tornado.escape import native_str
from utils.logger import logger

class TCPConnectionDelegage(object):
	def on_connect(self):
		pass

	def on_timeout(self):
		pass

	def on_receive(self, data):
		pass

	def on_write_complete(self):
		pass

	def on_close(self):
		pass

	def send(self, data):
		if not self.stream.closed():
			self.stream.write(data, stack_context.wrap(self.on_write_complete))
		else:
			raise Exception("connection is broken.")

	def __init__(self):
		self.stream = None
		self.address = None
		self.conn = None

	def close(self):
		if self.stream is not None:
			self.stream.close()

class TCPConnection(object):
	def __init__(self, stream, address, delegate = TCPConnectionDelegage()):
		self.delegate = delegate
		self.stream = stream
		self.address = address
		self.address_family = stream.socket.family
		self.delegate.stream = stream
		self.delegate.address = address
		self.delegate.conn = self
		self.delegate.on_connect()
		self.stream.set_close_callback(self._on_connection_close)
		self._message_body_callback = stack_context.wrap(self._on_receive_body)
		self._message_header_callback = stack_context.wrap(self._on_receive_header)
		self.stream.read_bytes(2, self._message_header_callback, partial=True)

	def _on_timeout(self):
		logger().i("connect timeout")
		self.delegate.on_timeout()

	def _on_connection_close(self):
		logger().i("client is disconnect %s", str(self.address))
		self.delegate.on_close()

	def _on_receive_header(self, header):
		try:
			bodylen = struct.unpack('<H', header)[0] #使用的是小端
			logger().i("receive msg len is %d", bodylen)
			self.stream.read_bytes(bodylen, self._message_body_callback, partial=True)
		except Exception as ex:
			raise ex

	def _on_receive_body(self, data):
		try:
			self.delegate.on_receive(data)
			self.stream.read_bytes(2, self._message_header_callback, partial=True)
		except Exception as ex:
			logger().e("on_receive: %s", str(ex))
			pass

class TCPBaseServer(TCPServer):
	def __init__(self, io_loop=None, delegate=None, **kwargs):
		TCPServer.__init__(self, io_loop=io_loop, **kwargs)
		assert isinstance(delegate, TCPConnectionDelegage), "delegate must be implement TCPConnectionDelegage"
		self.delegate = delegate

	def handle_stream(self, stream, address):
		if self.delegate is None:
			TCPConnection(stream, address, TCPConnectionDelegage())
		else:
			TCPConnection(stream, address, self.delegate)
		

	def run(self, port):
		self.listen(port)


def main():
	server = TCPBaseServer()
	server.listen(8001)
	logger().i("server runing at %d", 8001)
	ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	try:
		main()
	except Exception as ex:
		logger().excpt("Ocurred Exception: %s", str(ex))
		quit()
