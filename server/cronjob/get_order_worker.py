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
    #print('''*********** {} is running ***********'''.format(user['username']))

    orderOffset = 0
    updatedAfter, exception = orderDao.getMaxUpdatedAt(user)
    if (exception != None):
      print(exception)
      return

    while(True):
      # Get Lazada orders and insert to our dataBase
      exception = self.performGetOrders(user, orderOffset, updatedAfter);
      if exception != None:
        print(exception)
        return

      orderOffset += LazadaAPI.LIMIT

  #-----------------------------------------------------------------------------
  # Get Lazada orders and insert to our dataBase
  # Return Boolean
  #-----------------------------------------------------------------------------
  def performGetOrders(self, user, orderOffset, updatedAfter):
    # Get lazada orders by offset
    orders, exception = lazadaOrderApi.getOrdersByUpdatedAfter(user, orderOffset, updatedAfter)
    if (exception != None):
      return exception
    if (len(orders) <= 0):
      return '''{}: Reach to the end with updatedAfter: {}, offset: {}'''.format(user['username'], updatedAfter, orderOffset)

    #print('''{}: Get lazada orders with updatedAfter: {} and Offset: {} is successful'''.format(user['username'], updatedAfter, orderOffset))

    # Process data
    for order in orders:
      isOrderExist, exception = orderDao.isOrderExist(user, order['OrderId'])
      if (exception != None):
        return exception

      # Insert or update Order
      if (isOrderExist == False):
        result, exception = orderDao.insert(user, ConvertHelper.convertLazadaOrderToOrder(order))
        if (exception != None):
          return exception
      else:
        result, exception = orderDao.updateOrder(user, ConvertHelper.convertLazadaOrderToOrder(order))
        if (exception != None):
          return exception

      # Get OrderItems
      orderItems, exception = lazadaOrderApi.getOrderItems(user, order['OrderId'])
      if (exception != None):
        return exception
      # Get current OrderItems
      currentOrderItems, exception = orderItemDao.getOrderItemByOrderId(user, order['OrderId'])
      if (exception != None):
        return exception
      # Insert OrderItems
      exception = self.performInsertOrderItems(user, order, currentOrderItems, orderItems)
      if (exception != None):
        return exception

    return None

  #-----------------------------------------------------------------------------
  # Insert new if not exist in database else should update
  # Return Boolean, Exception
  #-----------------------------------------------------------------------------
  def performInsertOrderItems(self, user, order, currentOrderItems, orderItems):
    if (orderItems == None or len(orderItems) <= 0):
      return '''Lazada orderItems is empty or null, check order_id: {}'''.format(order['OrderId'])

    # Get current orderItem
    for orderItem in orderItems:
      isExist = self.isMatched(orderItem['OrderItemId'], currentOrderItems)
      if (isExist == True):
        result, exception = orderItemDao.update(user, ConvertHelper.convertLazadaOrderItemToOrderItem(orderItem))
        if (exception != None):
          return exception
      else:
        result, exception = orderItemDao.insert(user, ConvertHelper.convertLazadaOrderItemToOrderItem(orderItem))
        if (exception != None):
          return exception

    return None

  #-----------------------------------------------------------------------------
  # Checking orderItem is exist in our database (currentOrderItems)
  # Return Boolean
  #-----------------------------------------------------------------------------
  def isMatched(self, orderItemId, currentOrderItems):
    if (currentOrderItems == None or len(currentOrderItems) <= 0):
      return False

    for orderItem in currentOrderItems:
      if (orderItem['order_item_id'] == orderItemId):
        return True

    return False












