from database.sku_dao import SkuDao
from database.user_dao import UserDao
from managers.user_manager import UserManager
from lazada_api.lazada_order_api import LazadaOrderApi
from managers.response_helper import ResponseHelper


class OrderManager(object):

	def getOrder(self, order, user):

		# Validate SKU by lazada API
		lazadaSkuApi = LazadaOrderApi()
		lazadaOrder = lazadaSkuApi.getOrder(order, user)
		if not lazadaOrder:
			return ResponseHelper.generateErrorResponse("Can't access to Lazada service")

		return ResponseHelper.generateSuccessResponse(lazadaOrder)

	def getOrderItems(self, order, user):

		# Validate SKU by lazada API
		lazadaSkuApi = LazadaOrderApi()
		lazadaOrderItems = lazadaSkuApi.getOrderItems(order, user)
		if not lazadaOrderItems:
			return ResponseHelper.generateErrorResponse("Can't access to Lazada service")

		return ResponseHelper.generateSuccessResponse(lazadaOrderItems)