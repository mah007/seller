import time
import requests
import threading
from lxml import html
from config import ConstantConfig, LazadaAPI
from database.constant_dao import ConstantDao
from lazada_api.lazada_product_api import LazadaProductApi
from database.product_dao import ProductDao
from utils.convert_helper import ConvertHelper

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

    # Get offset: must not error
    productOffsetConstant = constantDao.getConstant(user, ConstantConfig.PRODUCT_OFFSET)
    if 'error' in productOffsetConstant:
      print(productOffsetConstant)
      return

    productOffset = productOffsetConstant['value']
    while(True):
      # Get Lazada products and insert to our dataBase
      result, exceptionOrLength = self.getProductFromLazadaAndInsertToOurDatabase(user, productOffset);
      if result == False:
        print(exceptionOrLength)
        return

      print('''{} Get lazada products with offset {} is successful'''.format(user['lazada_user_name'], productOffset))

      # Addition offset and update to constant: must not error
      productOffset += exceptionOrLength
      result = constantDao.updateConstant(user, ConstantConfig.PRODUCT_OFFSET, productOffset)
      if 'error' in result:
        print(result)
        return

  #-----------------------------------------------------------------------------
  # Get Lazada products and insert to our dataBase
  # Return Boolean, Exception/Length
  #-----------------------------------------------------------------------------
  def getProductFromLazadaAndInsertToOurDatabase(self, user, productOffset):
    # Get lazada products by offset
    products, totalProducts = lazadaProductApi.getProducts(user, productOffset)
    if 'error' in products:
      return False, products

    # This would never happen
    if productOffset > totalProducts:
      result = '''{} Something wrong with Offset: {} and totalProducts: {}'''.format(productOffset, totalProducts)
      return False, result

    # That is finish
    if len(products) <= 0 or productOffset == totalProducts:
      result = '''{} Reach to the end with offset {}'''.format(user['lazada_user_name'], productOffset)
      return False, result

    # Insert or update to our database
    recordCount = 0
    for product in products:
      product = ConvertHelper.convertLazadaProductToProduct(product)

      # Do check exist to avoid insert in duplication
      isProductExist, errorException = productDao.isProductExist(user, product['shop_sku'])
      if errorException != None:
        return False, errorException

      result = {}
      if isProductExist == True:
        result = productDao.updateProductWithLazadaProduct(user, product)
      else:
        result = productDao.insert(user, product)
        recordCount += 1
      if 'error' in result:
        return False, result

    return True, recordCount













