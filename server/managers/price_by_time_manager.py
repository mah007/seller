from database.product_dao import ProductDao
from database.price_by_time_dao import PriceByTimeDao
from managers.manager_helper import ManagerHelper
from utils.response_utils import ResponseUtils
from managers.response_helper import ResponseHelper

class PriceByTimeManager(object):

  def initialize(self):
    priceByTime = PriceByTimeDao()
    priceByTime.createTable()

  #-----------------------------------------------------------------------------
  # insert a new price balancer
  #-----------------------------------------------------------------------------
  def insert(self, sku, token):
    user = ManagerHelper.validateToken(token)
    if 'error' in user:
      return user

    #Valide product by Sku
    productDao = ProductDao()
    product, exception = productDao.getProductBySellerSku(user, sku);
    if exception != None:
      return ResponseUtils.generateErrorResponse(exception)

    # Add missing arguments and insert to our database
    sku['name'] = product['name'].encode('utf-8')
    sku['link'] = product['url'].encode('utf-8')
    sku['special_price'] = 0 #product['special_price']

    priceByTime = PriceByTimeDao()
    result = priceByTime.insert(sku, user)
    if 'error' in result:
      return ResponseUtils.generateErrorResponse(result['error'])
    else:
      return ResponseUtils.generateSuccessResponse()

  #-----------------------------------------------------------------------------
  # update price balancer's info
  #-----------------------------------------------------------------------------
  def update(self, sku, token):
    user = ManagerHelper.validateToken(token)
    if 'error' in user:
      return user

    priceByTime = PriceByTimeDao()
    result = priceByTime.update(sku, user)
    if 'error' in result:
      return ResponseUtils.generateErrorResponse(result['error'])
    else:
      return ResponseUtils.generateSuccessResponse()

  #-----------------------------------------------------------------------------
  # delete a price balancer
  #-----------------------------------------------------------------------------
  def delete(self, sku, token):
    user = ManagerHelper.validateToken(token)
    if 'error' in user:
      return user

    priceByTime = PriceByTimeDao()
    result = priceByTime.delete(sku, user)
    if 'error' in result:
      return ResponseUtils.generateErrorResponse(result['error'])
    else:
      return ResponseUtils.generateSuccessResponse()

  #-----------------------------------------------------------------------------
  # get all price by time
  #-----------------------------------------------------------------------------
  def getAll(self, token):
    user = ManagerHelper.validateToken(token)
    if 'error' in user:
      return user

    priceByTime = PriceByTimeDao()
    result = priceByTime.getAll(user)
    if result:
      return ResponseHelper.generateSuccessResponse(result)
    else:
      return ResponseHelper.generateErrorResponse("Error")





