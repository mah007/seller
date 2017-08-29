from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.exception_utils import ExceptionUtils


class HistoryDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS sku_history(
                id              INT AUTO_INCREMENT primary key NOT NULL,
                sku             TEXT     NOT NULL,
                enemy_json      TEXT            NOT NULL,
                user_id         INT              
                );'''
        DatabaseHelper.execute(query)


    # --------------------------------------------------------------------------
    # Insert history
    # --------------------------------------------------------------------------
    def insertHistory(self, sku, enemy_json, user):
        try:
            query = '''INSERT INTO sku_history(sku, enemy_json, user_id) VALUES ('{}', '{}','{}') '''.format(
                    sku['name'], enemy_json, user['id'])
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''Can't insert enemy''')

    # --------------------------------------------------------------------------
    def deleteHistoryBeforeInsert(self, sku):
        try:
            query = '''DELETE FROM sku_history WHERE sku =  '{}' '''.format(StringUtils.toString(sku['name']))
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''Unable to delete enemy''')
    # --------------------------------------------------------------------------
    # Get enemies
    # --------------------------------------------------------------------------
    def getEnemy(self, user):
        try:
            query = '''SELECT * from sku_history WHERE user_id = '{}' '''.format(user['id'])
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            rows = cur.fetchall()
            if not rows:
                conn.close()
                return ExceptionUtils.error('''Sku's enemy is not found''')

            enemies = []
            for row in rows:
                enemies.append({
                    'id': row[0],
                    'sku': row[1],
                    'enemy_json': row[2]
                })

            conn.close()
            return enemies
        except Exception as ex:
            return ExceptionUtils.error('''Get enemy's enemy failed: {}'''.format(str(ex)))









