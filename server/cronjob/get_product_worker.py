import threading
from config import ConstantConfig, LazadaAPI
from database.constant_dao import ConstantDao
from lazada_api.lazada_product_api import LazadaProductApi
from database.product_dao import ProductDao
from utils.convert_helper import ConvertHelper
from utils.timestamp_utils import TimestampUtils

constantDao = ConstantDao()
lazadaProductApi = LazadaProductApi()
productDao = ProductDao()

class GetProductWorker(threading.Thread):

  def __init__(self, kwargs):
    threading.Thread.__init__(self)
    self.kwargs = kwargs

  def run(self):
    user = self.kwargs['user']
    print('''*********** '{}' is running ***********'''.format(user['lazada_user_name']))

    # Get Last request datetime: must not error
    lastRequest, exception = constantDao.getConstant(user, ConstantConfig.PRODUCT_LAST_REQUEST)
    if (exception != None):
      print(exception)
      return

    offset = 0
    lastRequestDatetime = lastRequest['value']
    while(True):
      # Get Lazada products and insert to our dataBase
      result, exception = self.getProductFromLazadaAndInsertToOurDatabase(user, offset, lastRequestDatetime);
      if (result == False):
        print(exception)
        return

      # Get Product is done, exception must be message
      if (result == True and exception != None):
        self.updateConstant(user)
        if (exception != None):
          print(exception)
        return

      offset += LazadaAPI.LIMIT
      print("offset {}".format(offset))

  #-----------------------------------------------------------------------------
  # Update new request time to constant
  #-----------------------------------------------------------------------------
  def updateConstant(self, user):
    newResquestDatetime = TimestampUtils.getCurrentDatetime()
    exception = constantDao.updateConstant(user, ConstantConfig.PRODUCT_LAST_REQUEST, newResquestDatetime)
    if (exception != None):
      print(exception)
      return

  #-----------------------------------------------------------------------------
  # Get Lazada products and insert to our dataBase
  # Return Boolean, Exception/Length
  #-----------------------------------------------------------------------------
  def getProductFromLazadaAndInsertToOurDatabase(self, user, offset, lastRequest):
    # Get lazada products by offset
    products, exception = lazadaProductApi.getProductByUpdatedAfter(user, offset, lastRequest)
    if (exception != None):
      return False, exception

    # That is finish
    if len(products) <= 0:
      message = '''{} Reach to the end with UpdatedAfter: {}, offset: {}'''.format(user['lazada_user_name'], lastRequest, offset)
      return True, message

    # Insert or update to our database
    for product in products:
      product = ConvertHelper.convertLazadaProductToProduct(product)

      # Do check exist to avoid insert in duplication
      isProductExist, exception = productDao.isProductExist(user, product['shop_sku'])
      if (exception != None):
        return False, exception

      exception = None
      if (isProductExist == True):
        exception = productDao.updateProductWithLazadaProduct(user, product)
      else:
        exception = productDao.insert(user, product)
      if (exception != None):
        return False, exception

    return True, None













