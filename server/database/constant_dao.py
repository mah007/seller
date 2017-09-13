from database.database_helper import DatabaseHelper
from utils.exception_utils import ExceptionUtils


class ConstantDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS constant(
                id                  INT AUTO_INCREMENT primary key NOT NULL,
                constant_key        VARCHAR(15)      NOT NULL,
                value               INTEGER          NOT NULL,
                user_id             INTEGER          NOT NULL
                );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert constant
    # --------------------------------------------------------------------------
    def insertConstant(self, user, constant_key, value):
        query = '''INSERT INTO constant(constant_key, value, user_id) VALUES ('{}', '{}', '{}')
                '''.format(constant_key, value, user['id'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, Insert Constant exception {}'''.format(user['username'], user['id'], str(ex)))

    # --------------------------------------------------------------------------
    # Get constant
    # --------------------------------------------------------------------------
    def getConstant(self, user, constant_key):
        query = '''SELECT * FROM constant WHERE user_id = '{}' AND constant_key = '{}'
                '''.format(user['id'], constant_key)
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            row = cur.fetchone()
            if not row:
                conn.close()
                return ExceptionUtils.error('''User: {}-{}, Get constant not found, constant_key = {}'''.format(user['username'], user['id'], constant_key))

            result = {
                'value': row[2]
            }
            conn.close()
            return result
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, Get Constant exception {}'''.format(user['username'], user['id'], str(ex)))

    # --------------------------------------------------------------------------
    # check constant exist
    # --------------------------------------------------------------------------
    def isConstantExist(self, user, constant_key):
        query = '''SELECT * FROM constant WHERE user_id = '{}' and constant_key = '{}'
                '''.format(user['id'], constant_key)
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)
            constant = cur.fetchone()
            result = False if not constant else True;
            conn.close()
            return result
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, Insert Constant exception {}'''.format(user['username'], user['id'], str(ex)))

    # --------------------------------------------------------------------------
    # Update constant
    # --------------------------------------------------------------------------
    def updateConstant(self, user, constant_key, value):
        query = '''UPDATE constant SET value = '{}' WHERE constant_key = '{}' AND user_id = '{}'
                '''.format(value, constant_key, user['id'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, Get Order Constant exception {}'''.format(user['username'], user['id'], str(ex)))









