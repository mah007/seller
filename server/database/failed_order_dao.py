from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.exception_utils import ExceptionUtils


class FailedOrderDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS failed_order_management(
                id              INT AUTO_INCREMENT primary key NOT NULL,
                order_id        VARCHAR(50)     NOT NULL,
                order_number    VARCHAR(50)     NOT NULL,
                order_json      TEXT            NOT NULL,
                user_id         VARCHAR(30)     NOT NULL,
                created_at      VARCHAR(30)     NOT NULL,
                state           VARCHAR(20)     NOT NULL
                );'''
        DatabaseHelper.execute(query)


    # --------------------------------------------------------------------------
    # Insert order
    # --------------------------------------------------------------------------
    def insert(self, order, user):
        try:
            query = '''INSERT INTO failed_order_management(order_id, order_number, order_json, user_id, created_at, state) VALUES ('{}', '{}', 'None', '{}', '{}', '{}')'''.format(
                    order['OrderId'], order['OrderNumber'], user['lazada_user_id'], order['CreatedAt'], order['Statuses'][0])
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('Error')


    # --------------------------------------------------------------------------
    # Update Order State
    # --------------------------------------------------------------------------
    def updateState(self, order):
        query = '''UPDATE failed_order_management set state = 'ready_to_ship' WHERE id = '{}' '''.format(order['id'])
        DatabaseHelper.execute(query)


    def getFailedOrders(self):
        try:
            query = '''SELECT * FROM failed_order_management WHERE state = 'shipped' '''
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            orders = []
            rows = cur.fetchall()
            for row in rows:
                orders.append({
                    "id": row[0],
                    "order_id": row[1],
                    "order_number": row[2],
                    "order_json": row[3],
                    "user_id": row[4],
                    "created_at": row[5],
                    "state": row[6]
                })

            conn.close()
            return orders
        except Exception as ex:
            print(ex)
            return None

    def checkExistOrder(self, order):
        try:
            query = '''SELECT * FROM failed_order_management WHERE order_id = '{}' '''.format(order['order_id'])
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            rows = cur.fetchall()

            if not rows:
                return 0

            conn.close()
            return 1
        except Exception as ex:
            print(ex)
            return None   







