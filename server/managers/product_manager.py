from database.user_dao import UserDao
from database.product_dao import ProductDao
from database.constant_dao import ConstantDao
from lazada_api.lazada_product_api import LazadaProductApi
from utils.response_utils import ResponseUtils
from managers.response_helper import ResponseHelper
from lazada_api.lazada_api_helper import LazadaApiHelper
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
    # Insert product from Lazada with specific user
    #---------------------------------------------------------------------------
    def insertProductFromLazada(self, token):
        user = ManagerHelper.validateToken(token)
        if 'error' in user:
            return user

        constantDao = ConstantDao()
        productDao = ProductDao()
        lazadaProductApi = LazadaProductApi()
        flag = 1
        while (flag > 0):
            constant = constantDao.getConstant(user['id'], ConstantConfig.PRODUCT_OFFSET)

            offset = constant[0]['offset']
            result = lazadaProductApi.getProducts(user, constant)
            if result:
                for x in result:
                    offset = offset + 1
                    productDao.insert(x, user)
                    update = constantDao.updateConstantOffsetForProduct(offset, LazadaApiHelper.getCurrentUTCTime(), user)
            if(offset % 20 != 0):
                flag = -1

        return ResponseUtils.generateSuccessResponse(None)

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

    #-----------------------------------------------------------------------------
    # Search Product by name, seller sku, shop sku, brand and model
    #-----------------------------------------------------------------------------
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















