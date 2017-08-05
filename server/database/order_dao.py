from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.exception_utils import ExceptionUtils


class OrderDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS order_management(
                id              INT AUTO_INCREMENT primary key NOT NULL,
                order_id        VARCHAR(50)     NOT NULL,
                order_number    VARCHAR(50)     NOT NULL,
                order_json      TEXT            NOT NULL,
                user_id         INTEGER         NOT NULL,
                created_at      INTEGER         NOT NULL
                );'''
        DatabaseHelper.execute(query)


    # --------------------------------------------------------------------------
    # Insert order
    # --------------------------------------------------------------------------
    def insert(self, user, order):
        try:
            query = '''INSERT INTO order_management (order_id, order_number, order_json, user_id, created_at) VALUES ('{}', '{}', '{}', {}, {})'''.format(
                    order['order_id'], order['order_number'], order['order_json'], order['created_at'], user['id'])
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, Insert Order: {} failed: {}'''.format(user['id'], user['username'], order['order_id'], str(ex)))


    # --------------------------------------------------------------------------
    # Get order by order number
    # --------------------------------------------------------------------------
    def getOrderByOrderNumber(self, user, orderNumber):
        try:
            query = '''SELECT * from order_management WHERE user_id = '{}' AND order_number = '{}' '''.format(user['id'], orderNumber)
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            rows = cur.fetchall()
            if not rows:
                conn.close()
                return ExceptionUtils.error('''Order number: {} is not found'''.format(orderNumber))

            order = {}
            for row in rows:
                order['id'] = row[0]
                order['order_id'] = row[1]
                order['order_number'] = row[2]
                order['order_json'] = row[3]
                order['user_id'] = row[4]
                order['created_at'] = row[5]

            conn.close()
            return order
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, Get Order: {} failed: {}'''.format(user['id'], user['username'], orderNumber, str(ex)))












