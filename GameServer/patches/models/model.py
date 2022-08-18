# -*- coding: utf-8 -*-
# MySQLdb
#

from __future__ import absolute_import, division, with_statement

import copy
import itertools
import logging
import os
import time
from hashlib import md5
from patches.models import db

try:
	dbtype='sqlite'
	dbname="fn2010"
	theDB = db.database(dbname=dbtype)
	if dbtype == "mysql":
		theDB.connect(host="localhost",user="root",passwd="199010", charset="utf8")
	elif dbtype == "sqlite":
		theDB.connect(database=dbname)
	theDB.use_database(dbname)
	theDB.execute('CREATE DATABASE IF NOT EXISTS `fn2010` DEFAULT CHARSET utf8 COLLATE utf8_general_ci')
except Exception as e:
	raise e

class BaseModel(object):
	"""docstring for BaseModel"""

	def __init__(self):
		super(BaseModel, self).__init__()
		pass

	def get_all(self):
		try:
			r = lambda result, cursor : [x for x in cursor.fetchall()]
			theDB.query('select * from ' + self.tablename, r)
			return r
		except IndexError:
			pass

	def count(self):
		return sdb.query('select count(*)  as total from ' + self.tablename)[0]['total']	

class UserModel(BaseModel):
	"""docstring for UserModel"""
	def __init__(self):
		super(UserModel, self).__init__()
		self.tablename = 'tb_user'
		sql = """
			CREATE TABLE IF NOT EXISTS `tb_user` (
			`id` smallint(6) unsigned NOT NULL AUTO_INCREMENT,
     		`name` varchar(32) NOT NULL DEFAULT '',
  			`password` varchar(32) NOT NULL DEFAULT '',
  			PRIMARY KEY (`id`)
			) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
		"""
		theDB.execute(sql)
		if not self.has_user():
			self.add_new_user('admin', 'admin')
	def has_user(self):
		try:
			sql = 'SELECT id FROM %s LIMIT 1;'%(self.tablename)
			return theDB.query(sql) >0
		except IndexError:
			pass
		pass
	def add_new_user(self, name = '', pw = ''):
		if name and pw:
			try:
				pwd = md5(pw).hexdigest()
				sql = 'INSERT INTO tb_user (name, password) VALUES(%s,%s);'
				return theDB.execute(sql, name, pwd)
			except IndexError:
				pass
		pass

theUserModel = UserModel()