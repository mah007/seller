from database.sku_dao import SkuDao
from database.user_dao import UserDao
from database.order_dao import OrderDao
from database.constant_dao import ConstantDao
from database.failed_order_dao import FailedOrderDao
from managers.user_manager import UserManager
from lazada_api.lazada_order_api import LazadaOrderApi
from managers.order_helper import OrderHelper
from utils.response_utils import ResponseUtils
from managers.response_helper import ResponseHelper
import schedule
import time


class ConstantManager(object):
    def initialize(self):
        constantDao = ConstantDao()
        constantDao.createTable()

    def validateToken(self, token):
        userDao = UserDao()
        return userDao.getUser(token)

    #-----------------------------------------------------------------------------
    # Get Failed orders
    #-----------------------------------------------------------------------------
    def getConstantWithId(self, id):
        constantDao = ConstantDao()        
        result = constantDao.getConstant(id)

        if not result:
            return ResponseHelper.generateErrorResponse("Value is not exist!")

        return ResponseHelper.generateSuccessResponse(result)



    def checkValueExist(self, constant):
        constantDao = ConstantDao()
        result = constantDao.getConstant(constant)
        if (result['value'] == None):
            return ResponseHelper.generateErrorResponse("Value is not exist!")
        return ResponseHelper.generateSuccessResponse(result)

    













