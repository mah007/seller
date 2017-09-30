from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils


# TODO:
# 1. Should have a specific table for Account statement exception in case
# user POST duplicate account statment excel
#
# 2. Should have a DatabaseHelper.execute(query, value...) function

class AccountStatementDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS `account_statement` (
                id                              BIGINT AUTO_INCREMENT primary key NOT NULL,
                excel_url                       VARCHAR(100),
                start_date                      DATETIME,
                end_date                        DATETIME,
                sales_revenue                   DECIMAL(10,2),
                income                          DECIMAL(10,2) DEFAULT 0,
                created_at                      DATETIME,
                updated_at                      DATETIME,
                user_id                         BIGINT
                );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert an Account Statement
    # NOTE: UpdatedAt always have the same value with createdAt for the first time.
    # --------------------------------------------------------------------------
    def insert(self, user, invoice):
        query = '''INSERT INTO `account_statement`(excel_url, start_date,
                            end_date, sales_revenue, income,
                            created_at, updated_at, user_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
        conn = DatabaseHelper.getConnection()
        cur = conn.cursor()
        try:
            cur.execute(query, (invoice['excel_url'], invoice['start_date'],
                           invoice['end_date'],invoice['sales_revenue'],
                           invoice['income'], invoice['created_at'],
                           invoice['created_at'], invoice['user_id']))
            conn.commit()
            conn.close()
            return None
        except Exception as ex:
            conn.rollback()
            conn.close()
            return '''User: {}-{}, Insert-invoice: {}'''.format(user['username'], user['id'], str(ex))

    # --------------------------------------------------------------------------
    # Update an Account Statement
    # --------------------------------------------------------------------------
    def update(self, user, accountStatementId, income, updatedAt):
        query = ''' UPDATE invoice
                    SET income = {}, updated_at = '{}'
                    WHERE user_id = {} AND id = {}
                '''.format(income, updatedAt, user['id'], accountStatementId)
        try:
            result, exception = DatabaseHelper.execute(query)
            return exception
        except Exception as ex:
            return ''' User {}-{}, Update-Invoice: {} '''.format(user['username'], user['id'], str(ex))




