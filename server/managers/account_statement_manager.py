from database.user_dao import UserDao
from database.account_statement_dao import AccountStatementDao
from database.account_statement_exception_dao import AccountStatementExceptionDao
from utils.timestamp_utils import TimestampUtils
from utils.response_utils import ResponseUtils


class AccountStatementManager(object):

	def initialize(self):
	    accountStatementDao = AccountStatementDao()
	    accountStatementDao.createTable()
	    accountStatementExceptionDao = AccountStatementExceptionDao()
	    accountStatementExceptionDao.createTable()

	def validateToken(self, token):
		userDao = UserDao()
		user = userDao.getUser(token)
		if user == None:
			return ResponseUtils.generateErrorResponse("Invalid token")
		else:
			return user

	#-----------------------------------------------------------------------------
	# get all account statetment
	#-----------------------------------------------------------------------------
	def getAllAccountStatement(self, token):
		user = self.validateToken(token)
		if 'error' in user:
			return user

		accountStatementDao = AccountStatementDao()
		accountStatement, exception = accountStatementDao.getAllAccountStatement(user)

		if(exception != None):
			return ResponseUtils.generateErrorResponse(exception)
		return ResponseUtils.generateSuccessResponse(accountStatement)

	#-----------------------------------------------------------------------------
	# get all account statetment exception
	#-----------------------------------------------------------------------------
	def getAllAccountStatementException(self, token):
		user = self.validateToken(token)
		if 'error' in user:
			return user

		accountStatementExceptionDao = AccountStatementExceptionDao()
		result, exception = accountStatementExceptionDao.getAllAccountStatementException(user)
		if(exception != None):
			return ResponseUtils.generateErrorResponse(exception)
		return ResponseUtils.generateSuccessResponse(result)


















