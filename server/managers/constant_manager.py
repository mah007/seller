from database.user_dao import UserDao
from database.constant_dao import ConstantDao
from managers.response_helper import ResponseHelper

class ConstantManager(object):
    def initialize(self):
        constantDao = ConstantDao()
        constantDao.createTable()

    def validateToken(self, token):
        userDao = UserDao()
        return userDao.getUser(token)

    #-----------------------------------------------------------------------------
    # Get Constant with specific user_id
    #-----------------------------------------------------------------------------
    def getConstantWithUserId(self, user_id):
        constantDao = ConstantDao()        
        result = constantDao.getConstantWithUserId(user_id)

        if not result:
            return ResponseHelper.generateErrorResponse("Value is not exist!")

        return ResponseHelper.generateSuccessResponse(result)

    def checkValueExist(self, constant):
        constantDao = ConstantDao()
        result = constantDao.getConstant(constant)
        if (result['value'] == None):
            return ResponseHelper.generateErrorResponse("Value is not exist!")
        return ResponseHelper.generateSuccessResponse(result)



    













