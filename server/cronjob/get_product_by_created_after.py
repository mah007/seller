import time
import requests
import threading
from lxml import html
from config import ConstantConfig, LazadaAPI
from lazada_api.lazada_product_api import LazadaProductApi
from database.product_dao import ProductDao
from utils.convert_helper import ConvertHelper

lazadaProductApi = LazadaProductApi()
productDao = ProductDao()

class GetProductByCreatedAfterWorker(threading.Thread):

  def __init__(self, kwargs):
    threading.Thread.__init__(self)
    self.kwargs = kwargs

  def run(self):
    user = self.kwargs['user']
    print('''*********** '{}' is running ***********'''.format(user['lazada_user_name']))

    # TODO:
    # Handle product can be creating more than LIMIT (LazadaAPI.LIMIT)
    # within delay time (CronJob.GET_PRODUCT_TIME_INTEVAL).

    # Get lazada products by offset
    products, totalProducts = lazadaProductApi.getProductsWithCreatedAfter(user)
    if 'error' in products:
      print(products)
      return

    # There is no new products exist
    if len(products) <= 0:
      return

    # Insert or update to our database
    for product in products:
      product = ConvertHelper.convertLazadaProductToProduct(product)

      # Do check exist to avoid insert in duplication
      isProductExist, errorException = productDao.isProductExist(user, product['shop_sku'])
      if errorException != None:
        print(errorException)
        return

      result = {}
      if isProductExist == True:
        result = productDao.updateProductWithLazadaProduct(user, product)
      else:
        result = productDao.insert(user, product)
      if 'error' in result:
        print(result)
        return










