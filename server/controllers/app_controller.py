from database.user_dao import UserDao
from database.constant_dao import ConstantDao
from database.account_statement_dao import AccountStatementDao
from database.account_statement_exception_dao import AccountStatementExceptionDao
from config import ConstantConfig
from utils.lazada_api_helper import LazadaApiHelper

# Database instances
userDao = UserDao()
constantDao = ConstantDao()
accountStatementDao = AccountStatementDao()
accountStatementExceptionDao = AccountStatementExceptionDao()


class AppController(object):

    def initDatabase(self):
        # Init tables
        constantDao.createTable()
        accountStatementDao.createTable()
        accountStatementExceptionDao.createTable()
        # Init default values
        self.initDefaultConstantValue()

    #-----------------------------------------------------------------------------
    # Insert default constant for all user
    #-----------------------------------------------------------------------------
    def initDefaultConstantValue(self):
        users = userDao.getAll()
        if (users == None):
            return;

        # Insert Product Offset
        for user in users:
            # Check constant exist
            isProductOffsetExist, exception = constantDao.isConstantExist(user, ConstantConfig.PRODUCT_LAST_REQUEST)
            if (exception != None):
                print(exception)

            elif (isProductOffsetExist == False):
                fixStartDatetime = LazadaApiHelper.getFixedUpdatedAfterForCronJob()
                exception = constantDao.insertConstant(user, ConstantConfig.PRODUCT_LAST_REQUEST, fixStartDatetime)
                if (exception != None):
                    print(exception)








