from database.sku_dao import SkuDao
from database.user_dao import UserDao
from managers.user_manager import UserManager
from lazada_api.lazada_order_api import LazadaOrderApi
from managers.response_helper import ResponseHelper
from managers.order_helper import OrderHelper


class OrderManager(object):

	def validateToken(self, token):
		userDao = UserDao()
		user = userDao.getUser(token)
		if user == None:
			return ResponseHelper.generateErrorResponse("You should log out and login again to use this function !")
		else:
			return user

	#-----------------------------------------------------------------------------
	# Scan barcode
	#-----------------------------------------------------------------------------
	def scanBarcode(self, token, barcode):
		user = self.validateToken(token)
		if 'error' in user:
			return user

		# Get orderNumer
		orderNumber = OrderHelper.getOrderNumberFromBarcode(barcode)
		if not orderNumber:
			return ResponseHelper.generateErrorResponse("Barcode is invalid !")

		# Get order by orderNumber
		# Get orderItem by order
		# Return both of them and status of those think if there is any problems.

		return ResponseHelper.generateSuccessResponse(None)


	#-----------------------------------------------------------------------------
	# Get order by id
	#-----------------------------------------------------------------------------
	def getOrder(self, order, user):
		# Validate SKU by lazada API
		lazadaSkuApi = LazadaOrderApi()
		lazadaOrder = lazadaSkuApi.getOrder(order, user)
		if not lazadaOrder:
			return ResponseHelper.generateErrorResponse("Can't access to Lazada service")

		return ResponseHelper.generateSuccessResponse(lazadaOrder)


	#-----------------------------------------------------------------------------
	# Get orderItem by id
	#-----------------------------------------------------------------------------
	def getOrderItems(self, order, user):
		# Validate SKU by lazada API
		lazadaSkuApi = LazadaOrderApi()
		lazadaOrderItems = lazadaSkuApi.getOrderItems(order, user)
		if not lazadaOrderItems:
			return ResponseHelper.generateErrorResponse("Can't access to Lazada service")

		return ResponseHelper.generateSuccessResponse(lazadaOrderItems)








