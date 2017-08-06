from database.sku_dao import SkuDao
from database.user_dao import UserDao
from database.order_dao import OrderDao
from managers.user_manager import UserManager
from lazada_api.lazada_order_api import LazadaOrderApi
from managers.order_helper import OrderHelper
from utils.response_utils import ResponseUtils


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
            errorArray = ResponseUtils.convertToArryError("Token is invalid, please logout and login again !")
            return ResponseUtils.generateErrorResponse(errorArray)

        # Get orderNumer
        orderNumber = OrderHelper.getOrderNumberFromBarcode(barcode)
        if not orderNumber:
            errorArray = ResponseUtils.convertToArryError("Barcode is invalid !")
            return ResponseUtils.generateErrorResponse(errorArray)

        # Get order by orderNumber
        orderDao = OrderDao()
        order = orderDao.getOrderByOrderNumber(user, orderNumber)
        if 'error' in order:
            errorArray = ResponseUtils.convertToArryError(order['error'])
            return ResponseUtils.generateErrorResponse(errorArray)

        # Parse to ladaza format
        order = OrderHelper.convertOrderToLazadaOrder(order)
        # Get orderItem by order
        lazadaOrderApi = LazadaOrderApi()
        lazadaOrderItems = lazadaOrderApi.getOrderItems(order, user)
        if 'error' in lazadaOrderItems:
            errorArray = ResponseUtils.convertToArryError(lazadaOrderItems['error'])
            return ResponseUtils.generateErrorResponse(errorArray)

        # Return success response
        result = {
        "order": order,
        "orderItems": lazadaOrderItems
        }
        return ResponseUtils.generateSuccessResponse("Scane barcode is done", result)

    #-----------------------------------------------------------------------------
    # Refresh all orders
    #-----------------------------------------------------------------------------
    def refreshAllOrders(self, token):
        user = self.validateToken(token)
        if not user:
            errorArray = ResponseUtils.convertToArryError("Token is invalid, please logout and login again !")
            return ResponseUtils.generateErrorResponse(errorArray)

        # Delete all old orders first
        orderDao = OrderDao()
        result = orderDao.deleteAllOrders(user)
        if 'error' in result:
            errorArray = ResponseUtils.convertToArryError(result['error'])
            return ResponseUtils.generateErrorResponse(errorArray)

        # Get all orders from lazada
        lazadaOrderApi = LazadaOrderApi()
        orders = lazadaOrderApi.refreshAllOrder(user)
        if 'error' in orders:
            errorArray = ResponseUtils.convertToArryError(orders['error'])
            return ResponseUtils.generateErrorResponse(errorArray)

        # insert all orders into our database
        insertLogs = []
        for order in orders:
            insertLog = orderDao.insert(user, OrderHelper.convertLazadaOrderToOrder(order))
            if 'error' in insertLog:
                insertLogs.append(insertLog)

        # Check for success
        if len(insertLogs) > 0:
            return ResponseUtils.generateErrorResponse(insertLogs)
        else:
            return ResponseUtils.generateSuccessResponse("Refresh all Orders is done", None)


    #-----------------------------------------------------------------------------
    # Set order status to Ready-To-Ship
    #-----------------------------------------------------------------------------
    def setStatusToReadyToShip(self, token, orderItemIds, shippingProvider):
        user = self.validateToken(token)
        if not user:
            errorArray = ResponseUtils.convertToArryError("Token is invalid, please logout and login again !")
            return ResponseUtils.generateErrorResponse(errorArray)

        # Set status to Parked: this is necessary before set an order to Ready-To-Ship
        lazadaOrderApi = LazadaOrderApi()
        orders = lazadaOrderApi.setStatusToPackedByMarketplace(user, orderItemIds)
        if 'error' in orders:
            errorArray = ResponseUtils.convertToArryError(orders['error'])
            return ResponseUtils.generateErrorResponse(errorArray)

        # Set status to ready to ship
        orders = lazadaOrderApi.setStatusToReadyToShip(user, orderItemIds)
        if 'error' in orders:
            errorArray = ResponseUtils.convertToArryError(orders['error'])
            return ResponseUtils.generateErrorResponse(errorArray)

        return ResponseUtils.generateSuccessResponse("Set status to Ready-To-Ship is done", None)


    #-----------------------------------------------------------------------------
    # Get Failed orders
    #-----------------------------------------------------------------------------
    def getFailedOrders(self):
        # lazadaOrderApi = LazadaOrderApi()
        # lazadaOrders = lazadaOrderApi.getrOrders(user)
        orders = OrderDao()
        result = orders.getFailedOrders()
        if not result:
            return ResponseUtils.generateErrorResponse("Can't access to Lazada service")

        return ResponseUtils.generateSuccessResponse(result)


    #-----------------------------------------------------------------------------
    # Why insert order here????
    #-----------------------------------------------------------------------------
    def insertOrder(self, order, user):
        orderDao = OrderDao()
        orderDao.insert(order, user)
        return ResponseUtils.generateSuccessResponse(None)


    #-----------------------------------------------------------------------------
    # Update order state
    #-----------------------------------------------------------------------------
    def updataOrderState(self, order, token):
        user = self.validateToken(token)
        if 'error' in user:
            return user

        orderDao = OrderDao()
        orderdao.updateState(order)
        return ResponseUtils.generateSuccessResponse(None)












