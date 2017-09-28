import time
import schedule
from managers.manager_helper import ManagerHelper
from database.user_dao import UserDao
from database.order_dao import OrderDao
from database.order_item_dao import OrderItemDao
from database.product_dao import ProductDao
from lazada_api.lazada_order_api import LazadaOrderApi
from utils.response_utils import ResponseUtils
from utils.convert_helper import ConvertHelper
from importer import ImportExcel


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

    # Order       1--> order_number
    # Order       N--> Order item
    # Order item  N--> Sku
    def calculateEarning(self):
        user = ManagerHelper.validateToken(token)
        if not user:
            errorArray = ResponseUtils.convertToArryError("Token is invalid, please logout and login again !")

        orderDao = OrderDao()
        orderItemDao = OrderItemDao()
        productDao = ProductDao()
        importExcel = ImportExcel()

        earning = 0
        ordersmismatch = []

        datas = importExcel.getGeneralExchange()
        for data in datas:
            order, orderException = orderDao.getOrderByOrderNumber(user, data['order_number'])
            item, itemException = orderItemDao.getOrderItemByShopSku(user, data['sku'])

            # Check whether order is exist or not
            if(orderException != None):
                ordersmismatch.append({
                        'order': order,
                        'reason': orderException
                    })

            # Check whether order item is exist or not
            if(itemException != None):
                ordersmismatch.append({
                        'order': order,
                        'reason': itemException
                    })

            # Check whether item paid_price and sales_deliver is the same or not
            if(item['paid_price'] != data['sales_deliver']):
                reason = ("Order item price: '{}' doesn't match with sale deliver '{}' ").format(item['paid_price'], data['sales_deliver'])
                ordersmismatch.append({
                        'order': order,
                        'reason': reason
                    })

            # Check whether order had been delivered or not 
            if(order['statuses'] != 'delivered'):
                reason = ("Order with number: {} isn't delevired").format(order['order_number'])
                ordersmismatch.append({
                        'order': order,
                        reason: reason
                    })

            # Get original_price
            product, productException = productDao.getProductByShopSku(user, data)
            if(productException != None):
                ordersmismatch.append({
                        'order': order,
                        'reason': productException
                    })

            # Calculate earning then sum with the previous value
            earning = earning + (item['paid_price'] - (data['sum_of_fee'] + product['original_price']))

            # Check whether order had been update to calculated or not
            exceptionUpdate = orderDao.setCalculated(user, order)
            if(exceptionUpdate != None):
                ordersmismatch.append({
                        'order': order,
                        'reason': exceptionUpdate
                    })

            # Check whether order had been update to calculated or not
            uexceptionUpdate = orderItemDao.setEarned(user, item)
            if(exceptionUpdate != None):
                ordersmismatch.append({
                        'order': order,
                        'reason': exceptionUpdate
                    })

        result = []
        result.append({
            'earning': earning,
            'ordersmismatch': ordersmismatch
            })
        return result
























