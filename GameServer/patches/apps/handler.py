# -*- coding: utf-8 -*-
#
import os
import tornado.web
#from patches.models import model


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html",)

	def post(self):
		pass

#更新下载接口
class PatchesHandler(tornado.web.RequestHandler):
	def get(self,filename):
		self.set_header('Content-Type', 'application/octet-stream')
		self.set_header('Content-Disposition', 'attachment; filename=' + filename)
		patches_path = self.settings["patches_path"]
		with open(os.path.join(patches_path,filename)) as f:
			data = f.read()
			f.close()
			self.write(data)
		self.flush()

	def post(self):
		pass

class LoginHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("login.html",)
	def post(self):
		# try:
		# 	name = self.get_argument("name")
		# 	password = self.get_argument("pwd")
        #
		# 	susseccd = model.theUser.isexist_user(name, password)
		# 	if susseccd:
		# 		self.set_current_user(name, password)
		# 		self.redirect('/manager/index')
		# 		return
		# except Exception, e:
		# 	print e
		# 	pass
		# self.get()
		pass

class BlogHandler(tornado.web.RequestHandler):
	def get(self):
		pass