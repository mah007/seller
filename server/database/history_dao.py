from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.exception_utils import ExceptionUtils


class HistoryDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS enemy_management(
                id              INT AUTO_INCREMENT primary key NOT NULL,
                sku             VARCHAR(50)     NOT NULL,
                enemy_json      TEXT            NOT NULL
                );'''
        DatabaseHelper.execute(query)


    # --------------------------------------------------------------------------
    # Insert history
    # --------------------------------------------------------------------------
    def insertHistory(self, sku, enemy_json):
        try:
            query = '''INSERT INTO enemy_management(sku, enemy_json) VALUES ('{}', '{}')'''.format(
                    sku['name'], enemy_json)
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''Can't insert enemy''')

    # --------------------------------------------------------------------------
    def deleteHistoryBeforeInsert(self, sku):
        try:
            query = '''DELETE FROM enemy_management WHERE sku =  '{}' '''.format(StringUtils.toString(sku['name']))
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''Unable to delete enemy''')
    # --------------------------------------------------------------------------
    # Get enemies
    # --------------------------------------------------------------------------
    def getEnemy(self):
        try:
            query = '''SELECT * from enemy_management '''
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









