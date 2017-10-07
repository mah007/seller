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
  def changeOriginPrice(self, token, orderItems, accountStatementId):
    user, exception = Validation.validateToken(token)
    if (exception != None):
      return ResponseUtils.returnError(exception)

    orderItemDao = OrderItemDao()
    for orderItem in orderItems:
      # Get current OrderItem
      curOrderItem, exception = orderItemDao.getOrderItemByOrderItemId(user, orderItem['order_item_id'])
      if (exception != None):
        return ResponseUtils.returnError(exception)

      # Recompute earned/income and update
      commission = curOrderItem['actual_paid_price'] - curOrderItem['earned'] - curOrderItem['original_price']
      orderItem['earned'] = curOrderItem['actual_paid_price'] - (commission + orderItem['original_price'])
      exception = orderItemDao.changeOriginalPrice(user, orderItem)
      if (exception != None):
        return ResponseUtils.returnError(exception)

      # Update product's orginal price if its value is Zero
      if (curOrderItem['original_price'] == 0):
        productDao = ProductDao()
        exception = productDao.updateOriginalPriceByShopSku(user, orderItem['shop_sku'], orderItem['original_price'])
        if (exception != None):
          return ResponseUtils.returnError(exception)

    # Compute an account statement income
    income, exception = orderItemDao.getTotalEarningOfAccountStatement(user, accountStatementId)
    if (exception != None):
      return ResponseUtils.returnError(exception)

    # Recompute account statment income
    accountStatementDao = AccountStatementDao()
    updatedDate = TimestampUtils.getCurrentDatetime()
    exception = accountStatementDao.update(user, accountStatementId, income, updatedDate)
    if (exception != None):
      return ResponseUtils.returnError(exception)

    return ResponseUtils.generateSuccessResponse(None)


















