import time
from database.user_dao import UserDao


class UserManager(object):

	def initialize(self):
		userDao = UserDao()
		userDao.createTable()

	def getUser(self, token):
		userDao = UserDao()
		return userDao.getUser(token)

