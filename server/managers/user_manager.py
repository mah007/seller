import time
import jwt
import datetime
from database.user_dao import UserDao


class UserManager(object):

	def initialize(self):
		userDao = UserDao()
		userDao.createTable()


	def createUser(self, user):
		userDao = UserDao()
		return userDao.insert(user)


	def getUser(self, token):
		userDao = UserDao()
		return userDao.getUser(token)


	def login(self, user):
		userDao = UserDao()
		user = userDao.login(user)

		# Invalide user name or password
		if not user:
			return None

		# Generate token
		token = jwt.encode({'user' : 'username', 'createdAt': datetime.datetime.utcnow().isoformat()}, 'leoz')
		user['token'] = token.decode("utf-8")
		user = userDao.updateUserToken(user)
		if not user:
			return None # Error from update datebase.

		return user




