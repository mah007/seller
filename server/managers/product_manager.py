from database.user_dao import UserDao
from database.product_dao import ProductDao
from database.constant_dao import ConstantDao
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
    # Insert product from Lazada with specific user
    #--------------------------------------------------------------------------------------------
    def insertProductFromLazada(self, token):
        user = self.validateToken(token)
        if 'error' in user:
            return user
        constantDao = ConstantDao()
        productDao = ProductDao()
        lazadaProductApi = LazadaProductApi()
        flag = 1
        while (flag > 0):
            constant = constantDao.getConstantForProductWithUserId(user['id'])
          
            offset = constant[0]['offset']
            result = lazadaProductApi.getProducts(user, constant)
            if result:
                for x in result:
                    offset = offset + 1
                    productDao.insert(x, user)
                    update = constantDao.updateConstantOffsetForProduct(offset, LazadaApiHelper.getCurrentUTCTime(), user)
            if(offset % 20 != 0):
                flag = -1

        return ResponseHelper.generateSuccessResponse(None)

        















