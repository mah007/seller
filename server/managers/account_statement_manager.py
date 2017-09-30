from database.account_statement_dao import AccountStatementDao


class AccountStatementManager(object):
    def initialize(self):
        accountStatementDao = AccountStatementDao()
        accountStatementDao.createTable()