from database.price_balancer_dao import PriceBalancerDao
from managers.manager_helper import ManagerHelper
from lazada_api.lazada_sku_api import LazadaSkuApi
from utils.response_utils import ResponseUtils

class PriceBalancerManager(object):

  def initialize(self):
    priceBalancer = PriceBalancerDao()
    priceBalancer.createTable()

  #-----------------------------------------------------------------------------
  # insert a new price balancer
  #-----------------------------------------------------------------------------
  def insertPriceBalancer(self, sku, token):
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

    priceBalancer = PriceBalancerDao()
    result = priceBalancer.insert(sku, user)
    if 'error' in result:
      return ResponseUtils.generateErrorResponse(result['error'])

    return ResponseUtils.generateSuccessResponse()

  #-----------------------------------------------------------------------------
  # update price balancer's info
  #-----------------------------------------------------------------------------
  def updatePriceBalancer(self, sku, token):
    user = ManagerHelper.validateToken(token)
    if 'error' in user:
      return user

    priceBalancer = PriceBalancerDao()
    result = priceBalancer.update(sku, user)
    if 'error' in result:
      return ResponseUtils.generateErrorResponse(result['error'])

    return ResponseHelper.generateSuccessResponse()

  #-----------------------------------------------------------------------------
  # delete a price balancer
  #-----------------------------------------------------------------------------
  def deletePriceBalancer(self, sku, token):
    user = ManagerHelper.validateToken(token)
    if 'error' in user:
      return user

    priceBalancer = PriceBalancerDao()
    result = priceBalancer.delete(sku, user)
    if 'error' in result:
      return ResponseUtils.generateErrorResponse(result['error'])

    return ResponseHelper.generateSuccessResponse()

  #-----------------------------------------------------------------------------
  # get all price balancers
  #-----------------------------------------------------------------------------
  def getAll(self, token):
    user = ManagerHelper.validateToken(token)
    if 'error' in user:
      return user

    priceBalancer = PriceBalancerDao()
    result = priceBalancer.getAll(sku, user)
    if 'error' in result:
      return ResponseUtils.generateErrorResponse(result['error'])

    return ResponseHelper.generateSuccessResponse(result)





