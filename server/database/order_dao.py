from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.exception_utils import ExceptionUtils


class OrderDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS order_management(
                id              INT AUTO_INCREMENT primary key NOT NULL,
                order_id        VARCHAR(50)     NOT NULL,
                order_number    VARCHAR(50)     NOT NULL,
                price           VARCHAR(20)     NOT NULL,   # 113,000.00
                customer_name   VARCHAR(100)    NOT NULL,
                voucher_code    VARCHAR(50)     NOT NULL,
                voucher_price   VARCHAR(50)     NOT NULL,
                status          VARCHAR(100)    NOT NULL,
                created_at      VARCHAR(30)     NOT NULL,   # 2017-09-08 01:12:04
                updated_at      VARCHAR(30)     NOT NULL,   # 2017-09-08 01:12:04
                order_json      TEXT            NOT NULL,
                user_id         INTEGER         NOT NULL,
                );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert order
    # --------------------------------------------------------------------------
    def insert(self, user, order):
        query = '''INSERT INTO order_management(
                            order_id,
                            order_number,
                            price,
                            customer_name,
                            voucher_code,
                            voucher_price,
                            status,
                            created_at,
                            updated_at,
                            order_json,
                            user_id)
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                '''.format(order['order_id'], order['order_number'], order['price'],
                           order['customer_name'], order['voucher_code'],
                           order['voucher_price'], order['status'], order['created_at'],
                           order['updated_at'], order['order_json'], user['id'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, Insert-Order exception: {}'''.format(user['username'], user['id'], str(ex)))

    # --------------------------------------------------------------------------
    # Check Order exsits
    # --------------------------------------------------------------------------
    def isOrderExist(self, user, orderId):
        query = '''SELECT * FROM order_management WHERE order_id = '{}' AND user_id = '{}'' '''.format(orderId, user['id'])
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)
            order = cur.fetchone()
            result = False if not order else True;
            conn.close()
            return result
        except Exception as ex:
            print('''User: {}-{}, Check-Exist-Order exception: {}'''.format(user['username'], user['id'], str(ex)))
            return False

    # --------------------------------------------------------------------------
    # Get order by order number
    # --------------------------------------------------------------------------
    def getOrderByOrderNumber(self, user, orderNumber):
        query = '''SELECT *
                    FROM order_management
                    WHERE user_id = '{}' AND order_number = '{}'
                '''.format(user['id'], orderNumber)
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            row = cur.fetchone()
            if not row:
                conn.close()
                return ExceptionUtils.error('''User: {}-{}, Get Order: {} is not found'''.format(user['username'], user['id'], orderNumber))

            order = {
                'id': row[0],
                'order_id': row[1],
                'order_number': row[2],
                'price': row[3],
                'customer_name': row[4],
                'voucher_code': row[5],
                'voucher_price': row[6],
                'status': row[7],
                'created_at': row[8],
                'updated_at': row[9],
                'order_json': row[10],
                'user_id': row[11]
            }
            conn.close()
            return order
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, Order-Number: {}, Get-Order-By-Order-Number exception {}'''.format(user['username'], user['id'], orderNumber, str(ex)))

    # --------------------------------------------------------------------------
    # Update Order State
    # --------------------------------------------------------------------------
    def updateOrderState(self, user, order):
        query = '''UPDATE order_management
                    set status = '{}', updated_at = '{}', order_json = {}
                    WHERE id = '{}'
                '''.format(order['status'], order['updated_at'], order['order_json'], order['id'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, Order-Number: {}, Update-Order-State exception: {}'''.format(user['username'], user['id'], orderNumber, str(ex)))








