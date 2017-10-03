from database.user_dao import UserDao
from database.account_statement_dao import AccountStatementDao
from database.account_statement_exception_dao import AccountStatementExceptionDao
from database.order_item_dao import OrderItemDao
from database.product_dao import ProductDao
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

	#-----------------------------------------------------------------------------
	# Update account statement
	#-----------------------------------------------------------------------------
	def updateAccountStatement(self, accountStatement, token):
		user = self.validateToken(token)
		if 'error' in user:
			return user

		productDao = ProductDao()
		orderItemDao = OrderItemDao()

		# Update original price
		product, productException = productDao.getProductByShopSku(user, accountStatement['shop_sku'])
		if(productException != None):
			print("Product doesn't exists")
		else:
			result = productDao.updateProductPrice(accountStatement)

		orderItemDao.updateItemPrice(accountStatement)
		# Set OrderItem income:
      	# NOTE: Not do set if Product is not found => will calculate again next time
      	if (orderItem['earned'] == 0 and getProductException == None):
        	exception = orderItemDao.setIncome(user, order['order_id'], data['sku'], incomeOfAnOrderItem)
        if(exception != None):
          exceptions.append({'order_number': order['order_number'], 'reason': exception})
      	# Mark Order as Computed
      	if (order['calculated'] == 0):
        	exception = orderDao.markComputed(user, order['order_id'], accountStatement['id'])
        if (exception != None):
          exceptions.append({'order_number': order['order_number'], 'reason': exception})

		return ResponseUtils.generateSuccessResponse(None)


















