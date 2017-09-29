from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils


class InvoiceDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS `invoice` (
                id                              INT AUTO_INCREMENT primary key NOT NULL,
                excel_url                       VARCHAR(100),
                start_date                      VARCHAR(100),
                end_date                        VARCHAR(100),
                sales_revenue                   DECIMAL(10,2),
                income                          DECIMAL(10,2) DEFAULT 0,
                exception                       JSON DEFAULT NULL,
                created_at                      VARCHAR(300),
                updated_at                      VARCHAR(300),
                user_id                         VARCHAR(100)
                );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert invoice
    # --------------------------------------------------------------------------
    def insert(self, user, invoice):
        query = '''INSERT INTO `invoice`(excel_url, start_date,
                            end_date, sales_revenue, income,
                            exception, created_at, updated_at, user_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
        conn = DatabaseHelper.getConnection()
        cur = conn.cursor()
        try:
            cur.execute(query, (invoice['excel_url'], invoice['start_date'],
                           invoice['end_date'],invoice['sales_revenue'],
                           invoice['income'], invoice['exception'],
                           invoice['created_at'], invoice['updated_at'], invoice['user_id']))
            conn.commit()
            conn.close()
            return None, None
        except Exception as ex:
            conn.rollback()
            conn.close()
            return None, '''User: {}-{}, Insert-invoice: {}'''.format(user['username'], user['id'], str(ex))

    # --------------------------------------------------------------------------
    # Check invoice exsits
    # --------------------------------------------------------------------------
    def isInvoiceExist(self, user, invoiceId):
        query = '''SELECT * FROM `invoice` WHERE id = '{}' AND user_id = '{}' '''.format(invoiceId, user['id'])
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)
            invoice = cur.fetchone()
            result = False if not invoice else True;
            conn.close()
            return result, None
        except Exception as ex:
            return False, '''User: {}-{}, Check-invoice-Exist: {}'''.format(user['username'], user['id'], str(ex))

    def updateInvoice(self, user, invoiceId, income, exception, createdAt):
        query = ''' UPDATE invoice
                    SET income = {}
                    AND exception = '{}'
                    AND created_at = '{}'
                    WHERE user_id = {}
                    AND id = {}
                '''.format(income, exception, createdAt, user['id'], invoiceId)
        try:
            result, ex = DatabaseHelper.execute(query)
            if (ex != None):
                return ex
            else:
                return None
        except Exception as ex:
            return ''' User {}-{}, Update-Invoice: {} '''.format(user['username'], user['id'], str(ex))




