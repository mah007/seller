from database.user_dao import UserDao
from database.constant_dao import ConstantDao
from managers.response_helper import ResponseHelper
from config import ConstantConfig
from utils.lazada_api_helper import LazadaApiHelper


# TODO
# 1. Insert constant for all user in first time.
# 2. Insert constant for new user when sign up.


class ConstantManager(object):

    def initialize(self):
        constantDao = ConstantDao()
        constantDao.createTable()
        self.initDefaultValue(constantDao)

    def initDefaultValue(self, constantDao):
        userDao = UserDao()
        superAdmin = userDao.getSuperAdmin()
        if 'error' in superAdmin:
            print(superAdmin)
            return;

        # Insert Product Offset
        isProductOffsetExist, exception = constantDao.isConstantExist(superAdmin, ConstantConfig.PRODUCT_LAST_REQUEST)
        if (exception != None):
            print(exception)
        elif (isProductOffsetExist == False):
            fixStartDatetime = LazadaApiHelper.getFixedUpdatedAfterForCronJob()
            exception = constantDao.insertConstant(superAdmin, ConstantConfig.PRODUCT_LAST_REQUEST, fixStartDatetime)
            if (exception != None):
                print(exception)



















