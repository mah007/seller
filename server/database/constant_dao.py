from database.database_helper import DatabaseHelper
from utils.exception_utils import ExceptionUtils


class ConstantDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS constant(
                id                  INT AUTO_INCREMENT primary key NOT NULL,
                key                 VARCHAR(15)      NOT NULL,
                value               INTEGER          NOT NULL,
                user_id             INTEGER          NOT NULL
                );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert constant
    # --------------------------------------------------------------------------
    def insertConstant(self, user, key, value):
        query = '''INSERT INTO constant(key, value, user_id) VALUES ('{}', '{}', '{}') '''.format(
                    key, value, user['id'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, Insert Constant exception {}'''.format(user['username'], user['id'], str(ex)))

    # --------------------------------------------------------------------------
    # Get constant
    # --------------------------------------------------------------------------
    def getConstant(self, user, key):
        query = '''SELECT * FROM constant WHERE user_id = '{}' AND key = {} '''.format(user['id'], key)
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            row = cur.fetchone()
            if not row:
                conn.close()
                return ExceptionUtils.error('''User: {}-{}, Get constant not found, key = {}'''.format(user['username'], user['id'], key))

            result = {
                'value': row[3]
            }
            conn.close()
            return result
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, Get Constant exception {}'''.format(user['username'], user['id'], str(ex)))

    # --------------------------------------------------------------------------
    # Update constant
    # --------------------------------------------------------------------------
    def updateConstant(self, user, key, value):
        try:
            query = '''UPDATE constant SET value = '{}' WHERE key = '{}' AND user_id = '{}' '''.format(value, key, user['id'])
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, Get Order Constant exception {}'''.format(user['username'], user['id'], str(ex)))









