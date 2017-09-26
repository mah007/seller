import time
import requests
import threading
from lxml import html
from config import ConstantConfig, LazadaAPI
from database.constant_dao import ConstantDao
from lazada_api.lazada_order_api import LazadaOrderApi
from database.order_dao import OrderDao
from database.order_item_dao import OrderItemDao
from utils.convert_helper import ConvertHelper

constantDao = ConstantDao()
lazadaOrderApi = LazadaOrderApi()
orderDao = OrderDao()
orderItemDao = OrderItemDao()

class GetOrderWorker(threading.Thread):

  def __init__(self, kwargs):
    threading.Thread.__init__(self)
    self.kwargs = kwargs

  def run(self):
    user = self.kwargs['user']
    print('''*********** {} is running ***********'''.format(user['username']))

    # Get offset: must not error
    orderOffsetConstant = constantDao.getConstant(user, ConstantConfig.ORDER_OFFSET)
    if 'error' in orderOffsetConstant:
      print(orderOffsetConstant)
      return

    orderOffset = orderOffsetConstant['value']
    while(True):
      # Get Lazada orders and insert to our dataBase
      result, exception = self.performGetOrders(user, orderOffset);
      if result == False:
        print(exception)
        return

      # Addition offset and update to constant: must not error
      orderOffset += LazadaAPI.LIMIT
      result = constantDao.updateConstant(user, ConstantConfig.ORDER_OFFSET, orderOffset)
      if 'error' in result:
        print(result)
        return

  #-----------------------------------------------------------------------------
  # Get Lazada orders and insert to our dataBase
  # Return Boolean
  #-----------------------------------------------------------------------------
  def performGetOrders(self, user, orderOffset):
    # Get lazada orders by offset
    orders, exception = lazadaOrderApi.getOrders(user, orderOffset)
    if exception != None:
      return False, exception
    if len(orders) <= 0:
      return False, '''{}: Reach to the end with offset {}'''.format(user['username'], orderOffset)

    print('''{}: Get lazada orders with offset {} is successful'''.format(user['username'], orderOffset))

    # Insert or update to our database
    for order in orders:
      isOrderExist, exception = orderDao.isOrderExist(user, order['OrderId'])
      if (exception != None):
        return False, exception

      # Insert Order
      if isOrderExist == False:
        result, exception = orderDao.insert(user, ConvertHelper.convertLazadaOrderToOrder(order))
        if (exception != None):
          return False, exception

      # Get OrderItems
      orderItems, exception = lazadaOrderApi.getOrderItems(user, order['OrderId'])
      if (exception != None):
        return False, exception

      # Insert OrderItems
      for orderItem in orderItems:
        isOrderItemExist, exception = orderItemDao.isOrderItemExist(user, orderItem['OrderItemId'])
        if (exception != None):
          return False, exception
        if (isOrderItemExist == False):
          result, exception = orderItemDao.insert(user, ConvertHelper.convertLazadaOrderItemToOrderItem(orderItem))
          if (exception != None):
            return False, exception

    return True, None













