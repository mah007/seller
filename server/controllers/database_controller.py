from database.account_statement_dao import AccountStatementDao
from database.account_statement_exception_dao import AccountStatementExceptionDao

# Database instances
accountStatementDao = AccountStatementDao()
accountStatementExceptionDao = AccountStatementExceptionDao()


class DatabaseController(object):
  def initDatabase(self):
    accountStatementDao.createTable()
    accountStatementExceptionDao.createTable()
