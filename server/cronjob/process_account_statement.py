from database.account_statement_dao import AccountStatementDao
from utils.excel_utils import ExcelUitls
from database.product_dao import ProductDao
from database.order_dao import OrderDao
from database.order_item_dao import OrderItemDao
from database.account_statement_exception_dao import AccountStatementExceptionDao


# For caching memory
orderDao = OrderDao()
orderItemDao = OrderItemDao()
productDao = ProductDao()

class ProcessAccountStatement(threading.Thread):

  def __init__(self, kwargs):
    threading.Thread.__init__(self)
    self.kwargs = kwargs

  def run(self):
    user = self.kwargs['user']
    accountStatement = self.kwargs['account_statement']
    print('''*********** Process Account Statement for {} ***********'''.format(user['lazada_user_name']))

    earning = 0
    exceptions = []

    datas = ExcelUitls.getAccountStatement(accountStatement['excel_url'])
    for data in datas:
      # Get order
      order, exception = orderDao.getOrderByOrderNumber(user, data['order_number'])
      if (exception != None):
        exceptions.append({'order_number': data['order_number'], 'reason': orderException})
        earning = earning + (data['sales_deliver'] - data['sum_of_fee'])
        continue

      # Get OrderItem
      orderItems, exception = orderItemDao.getOrderItemByShopSku(user, order['order_id'], data['sku'])
      if (exception or len(orderItems) <= 0):
        exceptions.append({'order_number': data['order_number'], 'reason': orderException})
        earning = earning + (data['sales_deliver'] - data['sum_of_fee'])
        continue

      # Compute for only first OrderItem and update imcome for all
      orderItem = orderItems[0]

      # Check OrderItem >> paid_price and Lazada >> sales_deliver
      if (orderItem['paid_price'] != data['sales_deliver']):
        reason = ("Order-Item price: {} doesn't match with Lazada-Sale-Deliver {} ").format(orderItem['paid_price'], data['sales_deliver'])
        exceptions.append({'order_number': order['order_number'], 'reason': reason})
      # Check whether order had been delivered or not
      if ('delivered' not in order['statuses']):
        reason = ("Order-Number: {} isn't delevired, real status: {}").format(order['order_number'], order['statuses'])
        ordersmismatch.append({'order_number': order['order_number'], reason: reason})

      # Calculate OrderItem income:
      # Default value: orderItem['earned'] >> This OrderItem income has been computed
      # If not: calculate by formula: orderItem['paid_price'] - (data['sum_of_fee'] + product['original_price'])
      incomeOfAnOrderItem = orderItem['earned']
      if (incomeOfAnOrderItem == 0):
        product, exception = productDao.getProductByShopSku(user, data['sku'])
        if (exception != None):
          ordersmismatch.append({'order_number': order['order_number'], 'reason': exception})
          incomeOfAnOrderItem = data['sales_deliver'] - data['sum_of_fee']
        else:
          incomeOfAnOrderItem = orderItem['paid_price'] - (data['sum_of_fee'] + product['original_price'])

      earning = earning + incomeOfAnOrderItem

      # Set OrderItem income
      if (orderItem['earned'] == 0):
        exception = orderItemDao.setIncome(user, user, order['order_id'], data['sku'], incomeOfAnOrderItem)
        if(exception != None):
          exceptions.append({'order_number': order['order_number'], 'reason': exception})
      # Mark Order as Computed
      if (order['calculated'] == 0):
        exception = orderDao.markComputed(user, order['order_id'], accountStatement['id'])
        if (exception != None):
          exceptions.append({'order_number': order['order_number'], 'reason': exception})

    return earning, exceptions

  #---------------------------------------------------------------------------
  # Calculate earning
  #---------------------------------------------------------------------------
  def computeAccountStatement(self, accountStatement):












