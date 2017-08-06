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
                user_id         VARCHAR(30)         NOT NULL,
                created_at      VARCHAR(30)     NOT NULL,
                status          TEXT
                );'''
        DatabaseHelper.execute(query)


    # --------------------------------------------------------------------------
    # Insert order
    # --------------------------------------------------------------------------
    def insert(self, order, user):
        try:
            query = '''INSERT INTO order_management (order_id, order_number, order_json, user_id, created_at, status) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')'''.format(
                    order['OrderId'], order['OrderNumber'], 'None', user['lazada_user_id'], order['CreatedAt'], order['Statuses'][0])
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}, Insert Order: {} failed: {}'''.format(user['lazada_user_id'], order['OrderId'], str(ex)))


    # --------------------------------------------------------------------------
    # delete all order
    # --------------------------------------------------------------------------
    def deleteAllOrders(self, user):
        try:
            query = '''DELETE FROM order_management WHERE user_id = {} '''.format(user['id'])
            print(query)
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, Delete all orders is error: {}'''.format(user['id'], user['username'], str(ex)))


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


    # --------------------------------------------------------------------------
    # Update Order State
    # --------------------------------------------------------------------------
    # def updateState(self, order):
    #     query = '''UPDATE order_management set status = 'shipped' WHERE id = '{}' '''.format(order['id'])
    #     DatabaseHelper.execute(query)


    # def getFailedOrders(self):
    #     try:
    #         query = '''SELECT * FROM order_management WHERE status = 'pending' '''
    #         conn = DatabaseHelper.getConnection()
    #         cur = conn.cursor()
    #         cur.execute(query)

    #         orders = []
    #         rows = cur.fetchall()
    #         for row in rows:
    #             orders.append({
    #                 "Id": row[0],
    #                 "OrderId": row[1],
    #                 "OrderNumber": row[2],
    #                 "OrderJson": row[3],
    #                 "UserId": row[4],
    #                 "CreatedAt": row[5],
    #                 "Status": row[6]
    #             })

    #         conn.close()
    #         return orders
    #     except Exception as ex:
    #         print(ex)
    #         return None







