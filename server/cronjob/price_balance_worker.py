import time
import requests
import threading
from lxml import html
from config import ConstantConfig, LazadaAPI
from database.constant_dao import ConstantDao
from lazada_api.lazada_order_api import LazadaOrderApi
from database.order_dao import OrderDao

constantDao = ConstantDao()
lazadaOrderApi = LazadaOrderApi()
orderDao = OrderDao()

class GetOrderWorker(threading.Thread):

  def __init__(self, kwargs):
    threading.Thread.__init__(self)
    self.kwargs = kwargs

  def run(self):
    user = self.kwargs['user']
    print('''*********** {} is running ***********'''.format(user['lazada_user_name']))

    # Get offset: must not error
    orderOffsetConstant = constantDao.getConstant(user, ConstantConfig.ORDER_OFFSET)
    if 'error' in orderOffsetConstant:
      print(orderOffsetConstant)
      return

    orderOffset = orderOffsetConstant['value']
    while(True):
      # Get Lazada orders and insert to our dataBase
      result = self.getLazadaOrderAndInsertToOurDataBase(user, orderOffset);
      if result == False:
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
  def getLazadaOrderAndInsertToOurDataBase(self, user, orderOffset):
    # Get lazada orders by offset
    orders = lazadaOrderApi.getOrders(user, orderOffset)
    if 'error' in orders:
      print(orders)
      return False
    if len(orders) <= 0:
      print('''{} Reach to the end with offset {}'''.format(user['lazada_user_name'], orderOffset))
      return False

    print('''{} Get lazada orders with offset {} is successful'''.format(user['lazada_user_name'], orderOffset))

    # Insert or update to our database
    for order in orders:
      isOrderExist = orderDao.isOrderExist(user, order['OrderId'])
      result = {}
      if isOrderExist == True:
        result = orderDao.updateOrder(user, order)
      else:
        result = orderDao.insert(user, OrderHelper.convertLazadaOrderToOrder(order))
      if 'error' in result:
        print(result)
        return False

    return True













