from database.user_dao import UserDao
from database.account_statement_dao import AccountStatementDao
from database.account_statement_exception_dao import AccountStatementExceptionDao
from database.order_item_dao import OrderItemDao
from database.product_dao import ProductDao
from functions.validation import Validation
from utils.timestamp_utils import TimestampUtils
from utils.response_utils import ResponseUtils


class AccountStatementController(object):

  #-----------------------------------------------------------------------------
  # get all account statetment
  #-----------------------------------------------------------------------------
  def getAllAccountStatement(self, token):
    user, exception = Validation.validateToken(token)
    if (exception != None):
      return ResponseUtils.returnError(exception)

    accountStatementDao = AccountStatementDao()
    data, exception = accountStatementDao.getAll(user)
    if (exception != None):
      return ResponseUtils.returnError(exception)

    for accountSta in data:
      accountSta['start_date'] = TimestampUtils.getDateFromDatetime(accountSta['start_date'])
      accountSta['end_date'] = TimestampUtils.getDateFromDatetime(accountSta['end_date'])

    return ResponseUtils.returnSuccess(data)

  #-----------------------------------------------------------------------------
  # get all account statetment exception
  #-----------------------------------------------------------------------------
  def getAccountStatementInfo(self, token, accountStatementId):
    user, exception = Validation.validateToken(token)
    if (exception != None):
      return ResponseUtils.returnError(exception)

    asExceptionDao = AccountStatementExceptionDao()
    asExceptions, exception = asExceptionDao.getAll(user, accountStatementId)
    if (exception != None):
      return ResponseUtils.returnError(exception)

    orderItemDao = OrderItemDao()
    orderItems, exception = orderItemDao.getOrderItemByAccountStatement(user, accountStatementId)
    if (exception != None):
      return ResponseUtils.returnError(exception)

    result = {
      "exceptions": asExceptions,
      "orderItems": orderItems
    }
    return ResponseUtils.returnSuccess(result)

  #-----------------------------------------------------------------------------
  # Update account statement
  #-----------------------------------------------------------------------------
  def updateAccountStatement(self, accountStatement, token):
    user = self.validateToken(token)
    if 'error' in user:
      return user

    # productDao = ProductDao()
    # orderItemDao = OrderItemDao()

    # # Update original price
    # product, productException = productDao.getProductByShopSku(user, accountStatement['shop_sku'])
    # if(productException != None):
    #   print("Product doesn't exists")
    # else:
    #   result = productDao.updateProductPrice(accountStatement)

    # orderItemDao.updateItemPrice(accountStatement)
    # # Set OrderItem income:
  #   # NOTE: Not do set if Product is not found => will calculate again next time
  #   if (orderItem['earned'] == 0 and getProductException == None):
    #   exception = orderItemDao.setIncome(user, order['order_id'], data['sku'], incomeOfAnOrderItem)
  #   if(exception != None):
  #     exceptions.append({'order_number': order['order_number'], 'reason': exception})
  #   # Mark Order as Computed
  #   if (order['calculated'] == 0):
  #     exception = orderDao.markComputed(user, order['order_id'], accountStatement['id'])
  #   if (exception != None):
  #     exceptions.append({'order_number': order['order_number'], 'reason': exception})

    return ResponseUtils.generateSuccessResponse(None)


















