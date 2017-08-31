from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.exception_utils import ExceptionUtils


class HistoryDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS sku_history(
                id              INT AUTO_INCREMENT  primary key NOT NULL,
                sku             VARCHAR(500)        NOT NULL,
                enemy_json      VARCHAR(500)        NOT NULL,
                user_id         INTEGER             NOT NULL,
                status          INTEGER             NOT NULL,   -- Sate for indicated that whether AutoPriceWorker can update special price on Lazada.
                created_at      INTEGER             NOT NULL
                );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert history
    # --------------------------------------------------------------------------
    def insertHistory(self, history, sku, user):
        try:
            query = '''INSERT INTO sku_history(sku, enemy_json, user_id, status, created_at) VALUES ('{}', '{}', {}, {}, {}) '''.format(
                    sku['sku'], history['enemy_json'], user['id'], history['status'], history['created_at'])
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''Insert new history failed: {}'''.format(str(ex)))

    # --------------------------------------------------------------------------
    # Delete history
    # Delete histories with created time less than #millisecond
    # --------------------------------------------------------------------------
    def deleteHistories(self, sku, millisecond):
        try:
            query = '''DELETE FROM sku_history WHERE sku = '{}' and created_at < {} '''.format(StringUtils.toString(sku['sku'], millisecond))
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''Delete history failed: {}'''.format(str(ex)))

    # --------------------------------------------------------------------------
    # Get enemies
    # --------------------------------------------------------------------------
    def getAllHistory(self, user):
        try:
            query = '''SELECT * from sku_history WHERE user_id = '{}' ORDER BY created_at DESC '''.format(user['id'])
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            histories = []
            rows = cur.fetchall()
            if not rows:
                conn.close()
                return histories

            for row in rows:
                histories.append({
                    'id': row[0],
                    'sku': row[1],
                    'enemy_json': row[2],
                    'status': row[4]
                })

            conn.close()
            return histories
        except Exception as ex:
            return ExceptionUtils.error('''Get history failed: {}'''.format(str(ex)))









