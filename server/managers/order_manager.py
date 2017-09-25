import time
import schedule
from managers.manager_helper import ManagerHelper
from database.user_dao import UserDao
from database.order_dao import OrderDao
from database.order_item_dao import OrderItemDao
from lazada_api.lazada_order_api import LazadaOrderApi
from utils.response_utils import ResponseUtils
from utils.convert_helper import ConvertHelper


class OrderManager(object):
    def initialize(self):
        orderDao = OrderDao()
        orderDao.createTable()
        orderItemDao = OrderItemDao()
        orderItemDao.createTable()

    #---------------------------------------------------------------------------
    # Scan barcode
    #---------------------------------------------------------------------------
    def scanBarcode(self, token, barcode):
        user = ManagerHelper.validateToken(token)
        if not user:
            errorArray = ResponseUtils.convertToArryError("Token is invalid, please logout and login again !")
            return ResponseUtils.generateErrorResponse(errorArray)

        # Get orderNumer
        orderNumber = ConvertHelper.getOrderNumberFromBarcode(barcode)
        if not orderNumber:
            errorArray = ResponseUtils.convertToArryError("Barcode is invalid !")
            return ResponseUtils.generateErrorResponse(errorArray)

        # Get order by orderNumber
        orderDao = OrderDao()
        order, exception = orderDao.getOrderByOrderNumber(user, orderNumber)
        if exception != None:
            errorArray = ResponseUtils.convertToArryError(exception)
            return ResponseUtils.generateErrorResponse(errorArray)

        # Get orderItem by order
        orderItemDao = OrderItemDao()
        orderItems, exception = orderItemDao.getOrderItemByOrderId(user, order['order_id'])
        if exception != None:
            errorArray = ResponseUtils.convertToArryError(exception)
            return ResponseUtils.generateErrorResponse(errorArray)

        # Return success response
        result = {
            "order": order,
            "orderItems": orderItems
        }
        return ResponseUtils.generateSuccessResponse(result)

    #-----------------------------------------------------------------------------
    # Set order status to Ready-To-Ship
    #-----------------------------------------------------------------------------
    def setStatusToReadyToShip(self, token, orderItemIds, shippingProvider):
        user = ManagerHelper.validateToken(token)
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

















