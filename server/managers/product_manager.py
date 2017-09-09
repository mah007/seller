from database.user_dao import UserDao
from database.product_dao import ProductDao
from lazada_api.lazada_product_api import LazadaProductApi
from managers.order_helper import OrderHelper
from utils.response_utils import ResponseUtils
from managers.response_helper import ResponseHelper
from lazada_api.lazada_api_helper import LazadaApiHelper

class ProductManager(object):
    def initialize(self):
        prroductDao = ProductDao()
        prroductDao.createTable()

    def validateToken(self, token):
        userDao = UserDao()
        return userDao.getUser(token)


    def getAllProduct(self, token):
        user = self.validateToken(token)
        if 'error' in user:
            return user

        productDao = ProductDao()
        products = productDao.getAllProduct(user)
        return ResponseHelper.generateSuccessResponse(products)


    #--------------------------------------------------------------------------------------------
    # Insert products from Lazada with specific user
    #--------------------------------------------------------------------------------------------
    def insertProductFromLazada(self, token):
        user = self.validateToken(token)
        if 'error' in user:
            return user
        lazadaProductApi = LazadaProductApi()
        productDao = ProductDao()
        products = lazadaProductApi.getProducts(user)

        for product in products:
            productDao.insert(product, user)
        return ResponseHelper.generateSuccessResponse(None)

        # if products:
        #     for product in products:
        #         productDao.insert(product, user)
        #     return ResponseHelper.generateSuccessResponse(None)

        # return ResponseHelper.generateErrorResponse('Error while getting products')        

        















