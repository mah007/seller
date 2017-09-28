from database.user_dao import UserDao
from database.constant_dao import ConstantDao
from managers.response_helper import ResponseHelper
from config import ConstantConfig

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
        isProductOffsetExist = constantDao.isConstantExist(superAdmin, ConstantConfig.PRODUCT_OFFSET)
        if isProductOffsetExist == False:
            result = constantDao.insertConstant(superAdmin, ConstantConfig.PRODUCT_OFFSET, 0)
            if 'error' in result:
                print(result)



















