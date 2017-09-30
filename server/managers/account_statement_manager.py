from database.user_dao import UserDao
from database.account_statement_dao import AccountStatementDao
from database.account_statement_exception_dao import AccountStatementExceptionDao
from utils.timestamp_utils import TimestampUtils


class AccountStatementManager(object):

  def initialize(self):
    accountStatementDao = AccountStatementDao()
    accountStatementDao.createTable()
    accountStatementExceptionDao = AccountStatementExceptionDao()
    accountStatementExceptionDao.createTable()


















