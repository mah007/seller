from database.user_dao import UserDao
from database.order_dao import OrderDao
from database.failed_order_dao import FailedOrderDao
from database.constant_dao import ConstantDao
from managers.user_manager import UserManager
from lazada_api.lazada_order_api import LazadaOrderApi
from managers.order_helper import OrderHelper
from utils.response_utils import ResponseUtils
from managers.response_helper import ResponseHelper
from lazada_api.lazada_api_helper import LazadaApiHelper
import schedule
import time


class OrderManager(object):
    def initialize(self):
        orderDao = OrderDao()
        orderDao.createTable()
        failedOrderDao = FailedOrderDao()
        failedOrderDao.createTable()

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
    def getAllFailedOrders(self):
        failedOrderDao = FailedOrderDao()
        result = failedOrderDao.getFailedOrders()

        if not result:
            return ResponseHelper.generateErrorResponse("Can't access to Lazada service")

        return ResponseHelper.generateSuccessResponse(result)

    #--------------------------------------------------------------------------------------------
    # Insert order from Lazada with specific user
    #--------------------------------------------------------------------------------------------
    def insertOrderFromLazadaWithOneUser(self, user):
        constantDao = ConstantDao()
        failedOrderDao = FailedOrderDao()
        lazadaOrderApi = LazadaOrderApi()
        flag = 1
        while (flag > 0):
            constant = constantDao.getConstantForOrderWithUserId(user['user_id'])
            print(constant[0]['offset'])
            offset = constant[0]['offset']
            result = lazadaOrderApi.getOrders(user, constant)
            if result:
                for x in result:
                    offset = offset + 1
                    print(offset)
                    failedOrderDao.insert(x, user)
            if(offset % 25 != 0):
                flag = -1
            # dateTime = LazadaApiHelper.getCurrentUTCTime()
            constantDao.updateConstantOffsetForOrder(offset, LazadaApiHelper.getCurrentUTCTime(), user)

        return ResponseHelper.generateSuccessResponse(None)

    #-----------------------------------------------------------------------------
    # Update order state
    #-----------------------------------------------------------------------------
    def updateOrderState(self, order, token):
        user = self.validateToken(token)
        if 'error' in user:
            return user

        failedOrderDao = FailedOrderDao()
        failedOrderDao.updateState(order)
        return ResponseHelper.generateSuccessResponse(None)

















