from database.sku_dao import SkuDao
from database.user_dao import UserDao
from database.order_dao import OrderDao
from database.product_dao import ProductDao
from database.failed_order_dao import FailedOrderDao
from database.constant_dao import ConstantDao
from managers.user_manager import UserManager
from lazada_api.lazada_product_api import LazadaProductApi
from managers.order_helper import OrderHelper
from utils.response_utils import ResponseUtils
from managers.response_helper import ResponseHelper
from lazada_api.lazada_api_helper import LazadaApiHelper
import schedule
import time

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

        if products:
            for product in products:
                productDao.insert(product, user)
            return ResponseHelper.generateSuccessResponse(None)

        return ResponseHelper.generateErrorResponse('Error while getting products')        

        















