# -*- coding: utf-8 -*-
# 
import os.path

import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from patches.apps.handler import *

web_path = os.path.join(os.path.dirname(__file__), "patches")

define("port", default=8003, help="run on the given port", type=int)

settings = dict(
	template_path=os.path.join(web_path, "templates"),
	static_path=os.path.join(web_path, "static"),
	patches_path=os.path.join(web_path, "patches"),
	debug=True,
)

handlers = [
	(r"/", MainHandler),
	(r"/blog", BlogHandler),
	(r"/login", LoginHandler),
	(r"/patches/(.*)", PatchesHandler),
]

class Application(tornado.web.Application):
	def __init__(self):
		tornado.web.Application.__init__(self, handlers, **settings)

def main():
	tornado.options.parse_command_line()
	app = tornado.httpserver.HTTPServer(Application())
	app.listen(options.port)
	print ('listen....',options.port)
	tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
	try:
		main()
	except:
		quit()
