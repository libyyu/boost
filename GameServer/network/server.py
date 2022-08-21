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

	def notify_all(self, data):
		self.conn.notify_all(data, [self.conn])

	def __init__(self):
		self.stream = None
		self.address = None
		self.conn = None

	def close(self):
		if self.stream is not None:
			self.stream.close()

class TCPConnection(object):
	connections = set()
	def __del__(self):
		TCPConnection.connections.remove(self)
	def __init__(self, stream, address, delegate = TCPConnectionDelegage()):
		TCPConnection.connections.add(self)
		self.delegate = delegate
		self.stream = stream
		self.address = address
		self.address_family = stream.socket.family
		self.delegate.stream = stream
		self.delegate.address = address
		self.delegate.conn = self
		self.delegate.on_connect()
		self.stream.set_close_callback(self._on_connection_close)
		# self._message_body_callback = stack_context.wrap(self._on_receive_body)
		# self._message_header_callback = stack_context.wrap(self._on_receive_header)
		# self.stream.read_bytes(2, self._message_header_callback, partial=True)

	def notify_all(self, data, ignorelist = None):
		for conn in TCPConnection.connections:
			if ignorelist is None or conn not in ignorelist:
				conn.delegate.send(data)

	def _on_timeout(self):
		logger().i("connect timeout")
		self.delegate.on_timeout()

	def _on_connection_close(self):
		logger().i("client is disconnect %s", str(self.address))
		self.delegate.on_close()

	# def _on_receive_header(self, header):
	# 	try:
	# 		bodylen = struct.unpack('!H', header)[0] #使用的是大端
	# 		logger().i("receive msg len is %d", bodylen)
	# 		self.stream.read_bytes(bodylen, self._message_body_callback, partial=True)
	# 	except Exception as ex:
	# 		raise ex

	# def _on_receive_body(self, data):
	# 	try:
	# 		self.delegate.on_receive(data)
	# 		self.stream.read_bytes(2, self._message_header_callback, partial=True)
	# 	except Exception as ex:
	# 		logger().e("on_receive: %s", str(ex))
	# 		pass

	@gen.coroutine
	def _receive_message(self):
		while True:
			try:
				chunk = yield self.stream.read_bytes(2)
				if len(chunk) < 2:
					break
				bodylen = struct.unpack('!H', chunk)[0]
				chunk = yield self.stream.read_bytes(bodylen)
				while len(chunk) < bodylen:
					chunk += yield self.stream.read_bytes(bodylen - len(chunk))

				self.delegate.on_receive(chunk)
			except iostream.StreamClosedError:
				logger().w("client stream closed %s", str(self.address))
				break

class TCPBaseServer(TCPServer):
	def __init__(self, io_loop=None, delegate=None, **kwargs):
		TCPServer.__init__(self, io_loop=io_loop, **kwargs)
		assert isinstance(delegate, TCPConnectionDelegage), "delegate must be implement TCPConnectionDelegage"
		self.delegate = delegate

	@gen.coroutine
	def handle_stream(self, stream, address):
		if self.delegate is None:
			conn = TCPConnection(stream, address, TCPConnectionDelegage())
		else:
			conn = TCPConnection(stream, address, self.delegate)
		conn._receive_message()
		

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
