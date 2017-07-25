import time
import jwt
import datetime
import bcrypt
from database.user_dao import UserDao
from managers.response_helper import ResponseHelper
from utils.string_utils import StringUtils

class UserManager(object):

	def initialize(self):
		userDao = UserDao()
		userDao.createTable()


	def validateToken(self, token):
		userDao = UserDao()
		user = userDao.getUser(token)
		if user == None:
			return ResponseHelper.generateErrorResponse("Invalid token")
		else:
			return user


	# ----------------------------------------------------------------------------
	# Insert User
	# ----------------------------------------------------------------------------
	def insertUser(self, user, token):
		userToken = self.validateToken(token)
		if 'error' in userToken:
			return userToken

		userDao = UserDao()
		userAdmin = userDao.getAdminUser(userToken['id'])
		if userAdmin == None:
			return ResponseHelper.generateErrorResponse("Sorry! You are not allowed to insert new user!")

		userDB = userDao.getUserByUsername(user['username'])
		if (userDB != None):
			return ResponseHelper.generateErrorResponse("Username is already used")

		else:
			password = user['password'].encode('utf-8')
			user['password'] = bcrypt.hashpw(password, bcrypt.gensalt())
			userDao.insert(user)
			return ResponseHelper.generateSuccessResponse(user)


	# ----------------------------------------------------------------------------
	# Update Password
	# ----------------------------------------------------------------------------
	def updatePw(self, user, token):
		userDao = UserDao()
		userDB = userDao.getUserUpdatePW(token)
		if (userDB == None):
			return ResponseHelper.generateErrorResponse("Account not exist!")

		if bcrypt.checkpw(user['oldpass'].encode('utf-8'), userDB['password'].encode('utf-8')):
			password = user['newpass'].encode('utf-8')
			user['newpass'] = bcrypt.hashpw(password, bcrypt.gensalt())
			user['newpass'] = user['newpass'].decode('utf-8')
			user = userDao.updatePw(user, token)
			if not user:
				return ResponseHelper.generateErrorResponse("System error, please try again")

			return ResponseHelper.generateSuccessResponse(user)
		else:
			return ResponseHelper.generateErrorResponse("Password is invalid")


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
			user['password'] = None
			user = userDao.updateUserToken(user)
			if not user:
				return ResponseHelper.generateErrorResponse("System error, please try again")

			return ResponseHelper.generateSuccessResponse(user)
		else:
			return ResponseHelper.generateErrorResponse("Password is invalid")


	# ----------------------------------------------------------------------------
	# get all user
	# ----------------------------------------------------------------------------
	def getAll(self, token):
		userToken = self.validateToken(token)
		if 'error' in userToken:
			return userToken

		userDao = UserDao()
		userAdmin = userDao.getAdminUser(userToken['id'])
		if userAdmin == None:
			return ResponseHelper.generateErrorResponse("Sorry! You are not allowed to delete user!")

		userDao = UserDao()
		return userDao.getAll()


	# ----------------------------------------------------------------------------
	# Delete user
	# ----------------------------------------------------------------------------
	def deleteUser(self, user, token):
		userToken = self.validateToken(token)
		if 'error' in userToken:
			return userToken

		userDao = UserDao()
		userAdmin = userDao.getAdminUser(userToken['id'])
		if userAdmin == None:
			return ResponseHelper.generateErrorResponse("Sorry! You are not allowed to delete user!")

		userDao.deleteUser(user)
		return ResponseHelper.generateSuccessResponse(None)


	# ----------------------------------------------------------------------------
	# Update user
	# ----------------------------------------------------------------------------
	def updateUser(self, user, token):
		userToken = self.validateToken(token)
		if 'error' in userToken:
			return userToken

		else:			
			password = user['password'].encode('utf-8')
			user['password'] = bcrypt.hashpw(password, bcrypt.gensalt())
			user['password'] = user['password'].decode('utf-8')

		userDao = UserDao()
		userAdmin = userDao.getAdminUser(userToken['id'])
		if userAdmin == None:
			return ResponseHelper.generateErrorResponse("Sorry! You are not allowed to update user!")

		userDao.updateUser(user)
		return ResponseHelper.generateSuccessResponse(None)



