import time
import jwt
import datetime
import bcrypt
from database.user_dao import UserDao
from managers.response_helper import ResponseHelper


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


	# ----------------------------------------------------------------------------
	# Login
	# ----------------------------------------------------------------------------
	def login(self, user):
		userDao = UserDao()
		userDB = userDao.getUserByUsername(user['username'])
		if (userDB == None):
			return ResponseHelper.generateErrorResponse("Username is invalid")

		if bcrypt.checkpw(user['password'].encode('utf-8'), userDB['password'].encode('utf-8')):
			token = jwt.encode({'user' : 'username', 'createdAt': datetime.datetime.utcnow().isoformat()}, 'leoz')
			user['id'] = userDB['id']
			user['token'] = token.decode("utf-8")
			user['username'] = userDB['username'] # using lazada_user_name in database instead.
			user = userDao.updateUserToken(user)
			if not user:
				return ResponseHelper.generateErrorResponse("System error, please try again")

			return ResponseHelper.generateSuccessResponse(user)
		else:
			return ResponseHelper.generateErrorResponse("Password is invalid")


	def getAll(self):
		# user = self.validateToken(token)
		# if 'error' in user:
		# 	return user

		userDao = UserDao()
		return userDao.getAll()

	def deleteUser(self, user):
		userDao = UserDao()
		return userDao.deleteUser(user)


	def updateUser(self, user):
		userDao = UserDao()
		return userDao.updateUser(user)



