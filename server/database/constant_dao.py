from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.exception_utils import ExceptionUtils


class ConstantDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS constant(
                id              INT AUTO_INCREMENT primary key NOT NULL,
                name            VARCHAR(50)     NOT NULL,
                value           VARCHAR(50)         NOT NULL
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
    # Get constant with Id 
    # --------------------------------------------------------------------------
    def getConstant(self, constant):
        try:
            query = '''SELECT * FROM constant WHERE id = '{}' '''.format(constant['id'])
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            constant = []
            rows = cur.fetchall()
            for row in rows:
                constant.append({
                    "id": row[0],
                    "name": row[1],
                    "value": row[2]
                })

            conn.close()
            return constant
        except Exception as ex:
            print(ex)
            return None









