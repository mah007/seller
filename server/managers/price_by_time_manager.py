from database.price_by_time_dao import PriceByTimeDao
from managers.manager_helper import ManagerHelper
from lazada_api.lazada_sku_api import LazadaSkuApi
from utils.response_utils import ResponseUtils

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

    # Validate SKU by lazada API
    lazadaSkuApi = LazadaSkuApi()
    lazadaProduct = lazadaSkuApi.getSku(sku, user)
    if 'error' in lazadaProduct:
      return ResponseUtils.generateErrorResponse(lazadaProduct['error'])

    # Add missing arguments and insert to our database
    sku['name'] = lazadaProduct['Attributes']['name'].encode('utf-8')
    sku['link'] = lazadaProduct['Skus'][0]['Url'].encode('utf-8')

    priceByTime = PriceByTimeDao()
    result = priceByTime.insert(sku, user)
    if 'error' in result:
      return ResponseUtils.generateErrorResponse(result['error'])

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

    return ResponseUtils.generateSuccessResponse()

  #-----------------------------------------------------------------------------
  # get all price balancers
  #-----------------------------------------------------------------------------
  def getAll(self, token):
    user = ManagerHelper.validateToken(token)
    if 'error' in user:
      return user

    priceByTime = PriceByTimeDao()
    result = priceByTime.getAll(user)
    if 'error' in result:
      return ResponseUtils.generateErrorResponse(result['error'])

    return ResponseUtils.generateSuccessResponse(result)





