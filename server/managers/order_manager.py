from database.sku_dao import SkuDao
from database.user_dao import UserDao
from database.order_dao import OrderDao
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

    def validateToken(self, token):
        userDao = UserDao()
        return userDao.getUser(token)

    #---------------------------------------------------------------------------
    # Scan barcode
    #---------------------------------------------------------------------------
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

        # Parse to ladaza format: to get full info such as OrderItems
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

















