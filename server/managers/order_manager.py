from database.sku_dao import SkuDao
from database.user_dao import UserDao
from database.order_dao import OrderDao
from managers.user_manager import UserManager
from lazada_api.lazada_order_api import LazadaOrderApi
from managers.order_helper import OrderHelper
from managers.response_helper import ResponseHelper


class OrderManager(object):
    def initialize(self):
        orderDao = OrderDao()
        orderDao.createTable()

    def validateToken(self, token):
        userDao = UserDao()
        return userDao.getUser(token)


    #-----------------------------------------------------------------------------
    # Scan barcode
    #-----------------------------------------------------------------------------
    def scanBarcode(self, token, barcode):
        user = self.validateToken(token)
        if not user:
            errorArray = ResponseHelper.convertToArryError("Token is invalid, please logout and login again !")
            return ResponseHelper.generateErrorResponse(errorArray);

        # Get orderNumer
        orderNumber = OrderHelper.getOrderNumberFromBarcode(barcode)
        if not orderNumber:
            errorArray = ResponseHelper.convertToArryError("Barcode is invalid !")
            return ResponseHelper.generateErrorResponse(errorArray);

        # Get order by orderNumber
        orderDao = OrderDao()
        order = orderDao.getOrderByOrderNumber(user, orderNumber)
        if 'error' in order:
            errorArray = ResponseHelper.convertToArryError(order['error'])
            return ResponseHelper.generateErrorResponse(errorArray);

        # Parse to ladaza format
        order = OrderHelper.convertOrderToLazadaOrder(order)
        # Get orderItem by order
        lazadaOrderApi = LazadaOrderApi()
        lazadaOrderItems = lazadaOrderApi.getOrderItems(order, user)
        if 'error' in lazadaOrderItems:
            errorArray = ResponseHelper.convertToArryError(lazadaOrderItems['error'])
            return ResponseHelper.generateErrorResponse(errorArray);

        # Return success response
        result = {
        "order": order,
        "orderItems": lazadaOrderItems
        }
        return ResponseHelper.generateSuccessResponse("Scane barcode is done", result)

    #-----------------------------------------------------------------------------
    # Refresh all orders
    #-----------------------------------------------------------------------------
    def refreshAllOrders(self, token):
        user = self.validateToken(token)
        if not user:
            errorArray = ResponseHelper.convertToArryError("Token is invalid, please logout and login again !")
            return ResponseHelper.generateErrorResponse(errorArray);

        # Delete all old orders first
        orderDao = OrderDao()
        result = orderDao.deleteAllOrders(user)
        if 'error' in result:
            errorArray = ResponseHelper.convertToArryError(result['error'])
            return ResponseHelper.generateErrorResponse(errorArray);

        # Get all orders from lazada
        lazadaOrderApi = LazadaOrderApi()
        orders = lazadaOrderApi.refreshAllOrder(user)
        if 'error' in orders:
            errorArray = ResponseHelper.convertToArryError(orders['error'])
            return ResponseHelper.generateErrorResponse(errorArray);

        # insert all orders into our database
        insertLogs = []
        for order in orders:
            insertLog = orderDao.insert(user, OrderHelper.convertLazadaOrderToOrder(order))
            if 'error' in insertLog:
                insertLogs.append(insertLog)

        # Check for success
        if len(insertLogs) > 0:
            return ResponseHelper.generateErrorResponse(insertLogs)
        else:
            return ResponseHelper.generateSuccessResponse("Refresh all Orders is done", None)


	def getFailedOrders(self):
		# lazadaOrderApi = LazadaOrderApi()
		# lazadaOrders = lazadaOrderApi.getrOrders(user)
		orders = OrderDao()
		result = orders.getFailedOrders()
		if not result:
			return ResponseHelper.generateErrorResponse("Can't access to Lazada service")

		return ResponseHelper.generateSuccessResponse(result)

	def insertOrder(self, order, user):
		orderDao = OrderDao()
		orderDao.insert(order, user)
		return ResponseHelper.generateSuccessResponse(None)

	#-----------------------------------------------------------------------------
	# Update order state
	#-----------------------------------------------------------------------------
	def updataOrderState(self, order, token):
		user = self.validateToken(token)
		if 'error' in user:
			return user

		orderDao = OrderDao()
		orderdao.updateState(order)
		return ResponseHelper.generateSuccessResponse(None)











