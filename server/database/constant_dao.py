from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.exception_utils import ExceptionUtils


class ConstantDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS constant(
                id                     INT AUTO_INCREMENT primary key NOT NULL,
                name                   VARCHAR(50)     NOT NULL,
                date_time              VARCHAR(50)     NOT NULL,
                offset                 INTEGER         NOT NULL,
                user_id                VARCHAR(50)     NOT NULL
                );'''
        DatabaseHelper.execute(query)


    # --------------------------------------------------------------------------
    # Insert constant
    # --------------------------------------------------------------------------
    def insert(self, detail):
        try:
            query = '''INSERT INTO constant(name, value) VALUES ('{}', '{}')'''.format(detail['name'], detail['value'])
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('Error')     

    # --------------------------------------------------------------------------
    # Get constant for get order 
    # --------------------------------------------------------------------------
    def getConstantForOrderWithUserId(self, user_id):
        try:
            query = '''SELECT * FROM constant WHERE user_id = '{}' AND name = 'order' '''.format(user_id)
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            constant = []
            rows = cur.fetchall()
            for row in rows:
                constant.append({
                    "id": row[0],
                    "name": row[1],
                    "date_time": row[2],
                    "offset": row[3],
                    "user_id": row[4]
                })

            conn.close()
            return constant
        except Exception as ex:
            print(ex)
            return None

    # --------------------------------------------------------------------------
    # Get constant for get product
    # --------------------------------------------------------------------------
    def getConstantForProductWithUserId(self, user_id):
        try:
            query = '''SELECT * FROM constant WHERE user_id = '{}' AND name = 'product' '''.format(user_id)
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            constant = []
            rows = cur.fetchall()
            for row in rows:
                constant.append({
                    "id": row[0],
                    "name": row[1],
                    "date_time": row[2],
                    "offset": row[3],
                    "user_id": row[4]
                })
            conn.close()
            return constant
        except Exception as ex:
            print(ex)
            return None

    def getAllConstant(self):
        try:            
            query = '''SELECT * FROM constant '''
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            constant = []
            rows = cur.fetchall()
            for row in rows:
                constant.append({
                    "id": row[0],
                    "name": row[1],
                    "date_time": row[2],
                    "offset": row[3],
                    "user_id": row[4]
                })

            conn.close()
            return constant
        except Exception as ex:
            print(ex)
            return None

    def updateConstantOffsetForOrder(self, offset, dateTime, user):
        try:
            query = '''UPDATE constant SET offset = '{}', date_time = '{}' WHERE user_id = '{}' and name='order' '''.format(offset, dateTime, user['user_id'])
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('Error')    

    def updateConstantOffsetForProduct(self, offset, dateTime, user):
        try:
            query = '''UPDATE constant SET offset = '{}', date_time = '{}' WHERE user_id = '{}' and name = 'product' '''.format(offset, dateTime, user['id'])
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('Error')       








