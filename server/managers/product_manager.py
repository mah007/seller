from database.user_dao import UserDao
from database.product_dao import ProductDao
from database.constant_dao import ConstantDao
from lazada_api.lazada_product_api import LazadaProductApi
from utils.response_utils import ResponseUtils
from managers.response_helper import ResponseHelper
from utils.lazada_api_helper import LazadaApiHelper
from utils.convert_helper import ConvertHelper
from managers.manager_helper import ManagerHelper
from config import ConstantConfig

class ProductManager(object):

    def initialize(self):
        prroductDao = ProductDao()
        prroductDao.createTable()

    #---------------------------------------------------------------------------
    # Get all product
    #---------------------------------------------------------------------------
    def getProducts(self, token):
        user = ManagerHelper.validateToken(token)
        if 'error' in user:
            return user

        productDao = ProductDao()
        products = productDao.getProducts(user)
        return ResponseUtils.generateSuccessResponse(products)

    #---------------------------------------------------------------------------
    # Update product with new quantity and price
    #---------------------------------------------------------------------------
    def updateProduct(self, product, token):
        user = ManagerHelper.validateToken(token)
        if 'error' in user:
            return user

        productDao = ProductDao()
        productDao.updateProduct(product)
        return ResponseUtils.generateSuccessResponse(None)

    #---------------------------------------------------------------------------
    # Update product with new quantity and price
    #---------------------------------------------------------------------------
    def updateProductQuantity(self, product, token):
        user = ManagerHelper.validateToken(token)
        if 'error' in user:
            return user

        productDao = ProductDao()
        productDao.updateProductQuantity(product)
        return ResponseUtils.generateSuccessResponse(None)

    #---------------------------------------------------------------------------
    # Update product with new quantity and price
    #---------------------------------------------------------------------------
    def updateProductPrice(self, product, token):
        user = ManagerHelper.validateToken(token)
        if 'error' in user:
            return user

        productDao = ProductDao()
        productDao.updateProductPrice(product)
        return ResponseUtils.generateSuccessResponse(None)

    #---------------------------------------------------------------------------
    # Search Product by name, seller sku, shop sku, brand and model
    #---------------------------------------------------------------------------
    def searchProduct(self, token, searchKey):
        user = ManagerHelper.validateToken(token)
        if 'error' in user:
            return user

        productDao = ProductDao()
        result, exception = productDao.searchProduct(user, searchKey)
        if exception != None:
            return ResponseUtils.generateErrorResponse(exception)
        else:
            return ResponseUtils.generateSuccessResponse(result)















