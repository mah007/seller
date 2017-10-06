import threading
from utils.excel_utils import ExcelUitls
from utils.timestamp_utils import TimestampUtils
from database.product_dao import ProductDao
from database.order_dao import OrderDao
from database.order_item_dao import OrderItemDao
from database.account_statement_dao import AccountStatementDao
from database.account_statement_exception_dao import AccountStatementExceptionDao


# For caching memory
orderDao = OrderDao()
orderItemDao = OrderItemDao()
productDao = ProductDao()
accountStatementDao = AccountStatementDao();
accountStatementExceptionDao = AccountStatementExceptionDao();

class ProcessAccountStatement(threading.Thread):

  def __init__(self, kwargs):
    threading.Thread.__init__(self)
    self.kwargs = kwargs

  def run(self):
    user = self.kwargs['user']
    accountStatement = self.kwargs['account_statement']
    print('''*********** Process Account Statement for {} ***********'''.format(user['lazada_user_name']))

    # Compute income
    income, exceptions = self.process(user, accountStatement)

    # Update Account Statement income
    datetimeStr = TimestampUtils.getCurrentDatetime()
    updateException = accountStatementDao.update(user, accountStatement['id'], income, datetimeStr)
    if (updateException != None):
        print(updateException)

    # Add Account Statement exceptions
    print(exceptions)
    for exception in exceptions:
      insertException = accountStatementExceptionDao.insert(user, exception['order_number'], accountStatement['id'], exception['reason'], datetimeStr)
      if (insertException != None):
        print(insertException)


  #---------------------------------------------------------------------------
  # Calculate earning
  #---------------------------------------------------------------------------
  def process(self, user, accountStatement):
    income = 0
    exceptions = []

    datas = ExcelUitls.getAccountStatement(accountStatement['excel_url'])
    for data in datas:
      # Don't compute order have returned
      if (data['sales_return'] != 0):
        continue

      # Get order
      order, exception = orderDao.getOrderByOrderNumber(user, data['order_number'])
      if (exception != None):
        exceptions.append({'order_number': data['order_number'], 'reason': exception})
        income = income + (data['sales_deliver'] - data['sum_of_fee'])
        continue

      # Get OrderItem
      orderItems, exception = orderItemDao.getOrderItemByShopSku(user, order['order_id'], data['sku'])
      if (exception or len(orderItems) <= 0):
        exceptions.append({'order_number': data['order_number'], 'reason': exception})
        income = income + (data['sales_deliver'] - data['sum_of_fee'])
        continue

      # Compute for only first OrderItem and update imcome for all
      orderItem = orderItems[0]

      # Check OrderItem >> paid_price and Lazada >> sales_deliver
      if (orderItem['paid_price'] != data['sales_deliver']):
        reason = ("Order-Item-Paid-Price: {} doesn't match with Lazada-Sale-Deliver {} ").format(orderItem['paid_price'], data['sales_deliver'])
        exceptions.append({'order_number': order['order_number'], 'reason': reason})
      # Check whether order had been delivered or not
      if ('delivered' not in order['statuses']):
        reason = ("Status is: {}").format(order['statuses'])
        exceptions.append({'order_number': order['order_number'], 'reason': reason})
      # Check item_price and paid_price
      if (orderItem['item_price'] != orderItem['paid_price']):
        reason = ("Item-Price: {} doesn't matched with Paid-Price: {}").format(orderItem['item_price'], orderItem['paid_price'])
        exceptions.append({'order_number': order['order_number'], 'reason': reason})

      # Calculate OrderItem income:
      # Default value: orderItem['earned'] >> This OrderItem income has been computed
      # If not: calculate by formula: orderItem['paid_price'] - (data['sum_of_fee'] + product['original_price'])
      orderItemIncome = orderItem['earned']
      if (orderItemIncome == 0):
        product, getProductException = productDao.getProductByShopSku(user, data['sku'])
        if (exception != None):
          exceptions.append({'order_number': order['order_number'], 'reason': exception})
          orderItemIncome = data['sales_deliver'] - data['sum_of_fee']
        else:
          orderItemIncome = data['sales_deliver'] - (data['sum_of_fee'] + product['original_price'])

      # Actual income
      income = income + orderItemIncome

      # Set OrderItem income:
      if (orderItem['earned'] == 0):
        exception = orderItemDao.setIncome(user, order['order_id'], data['sku'], orderItemIncome, data['sales_deliver'])
        if (exception != None):
          exceptions.append({'order_number': order['order_number'], 'reason': exception})
      # Mark Order as Computed
      if (order['calculated'] == 0):
        exception = orderDao.markComputed(user, order['order_id'], accountStatement['id'])
        if (exception != None):
          exceptions.append({'order_number': order['order_number'], 'reason': exception})

    return income, exceptions












