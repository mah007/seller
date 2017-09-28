from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils


class OrderDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS `order` (
                id                              INT AUTO_INCREMENT primary key NOT NULL,
                order_id                        BIGINT,
                customer_first_name             VARCHAR(100),
                customer_lastName               VARCHAR(100),
                order_number                    BIGINT,
                payment_method                  VARCHAR(100),
                remarks                         VARCHAR(300),
                delivery_info                   VARCHAR(300),
                price                           DECIMAL(10,2),
                gift_option                     BOOLEAN DEFAULT NULL,
                gift_message                    VARCHAR(200),
                voucher_code                    VARCHAR(100),
                created_at                      DATETIME,
                updated_at                      DATETIME,
                address_billing                 TEXT DEFAULT NULL,
                address_shipping                TEXT DEFAULT NULL,
                national_registration_number    VARCHAR(300),
                items_count                     INTEGER,
                promised_shipping_times         VARCHAR(300),
                extra_attributes                VARCHAR(300),
                statuses                        TEXT DEFAULT NULL,
                voucher                         INTEGER,
                shipping_fee                    DECIMAL(10,2),
                user_id                         INTEGER,
                calculated                      INTEGER DEFAULT 0
                );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert order
    # --------------------------------------------------------------------------
    def insert(self, user, order):
        query = '''INSERT INTO `order`(order_id, customer_first_name,
                            customer_lastName, order_number, payment_method,
                            remarks, delivery_info, price, gift_option,
                            gift_message, voucher_code, created_at, updated_at,
                            address_billing, address_shipping, national_registration_number,
                            items_count, promised_shipping_times, extra_attributes,
                            statuses, voucher, shipping_fee, user_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        conn = DatabaseHelper.getConnection()
        cur = conn.cursor()
        try:
            cur.execute(query, (order['order_id'], order['customer_first_name'],
                           order['customer_lastName'],order['order_number'],
                           order['payment_method'], order['remarks'],
                           order['delivery_info'], order['price'],
                           order['gift_option'], order['gift_message'],
                           order['voucher_code'], order['created_at'],
                           order['updated_at'], order['address_billing'],
                           order['address_shipping'], order['national_registration_number'],
                           order['items_count'], order['promised_shipping_times'],
                           order['extra_attributes'], order['statuses'],
                           order['voucher'], order['shipping_fee'], user['id']))
            conn.commit()
            conn.close()
            return None, None
        except Exception as ex:
            conn.rollback()
            conn.close()
            return None, '''User: {}-{}, Insert-Order: {}'''.format(user['username'], user['id'], str(ex))

    # --------------------------------------------------------------------------
    # Check Order exsits
    # --------------------------------------------------------------------------
    def isOrderExist(self, user, orderId):
        query = '''SELECT id FROM `order` WHERE order_id = '{}' AND user_id = '{}' '''.format(orderId, user['id'])
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)
            order = cur.fetchone()
            result = False if not order else True;
            conn.close()
            return result, None
        except Exception as ex:
            return False, '''User: {}-{}, Check-Order-Exist: {}'''.format(user['username'], user['id'], str(ex))

    # # --------------------------------------------------------------------------
    # # Get order by order number
    # # --------------------------------------------------------------------------
    def getOrderByOrderNumber(self, user, orderNumber):
        query = '''SELECT *
                    FROM `order`
                    WHERE user_id = '{}' AND order_number = '{}'
                '''.format(user['id'], orderNumber)
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            row = cur.fetchone()
            if not row:
                conn.close()
                return None, '''User: {}-{}, Get Order: {} is not found'''.format(user['username'], user['id'], orderNumber)

            order = {
                "id": row[0],
                "order_id": row[1],
                "customer_first_name": row[2],
                "customer_lastName": row[3],
                "order_number": row[4],
                "payment_method": row[5],
                "remarks": row[6],
                "delivery_info": row[7],
                "price": row[8],
                "gift_option": row[9],
                "gift_message": row[10],
                "voucher_code": row[11],
                "created_at": row[12],
                "updated_at": row[13],
                "address_billing": row[14],
                "address_shipping": row[15],
                "national_registration_number": row[16],
                "items_count": row[17],
                "promised_shipping_times": row[18],
                "extra_attributes": row[19],
                "statuses": row[20],
                "voucher": row[21],
                "shipping_fee": row[22]
            }
            conn.close()
            return order, None
        except Exception as ex:
            return None, '''User: {}-{}, Order-Number: {}, Get-Order-By-Order-Number exception {}'''.format(user['username'], user['id'], orderNumber, str(ex))


    def setCalculated(self, user, order):
        query = ''' UPDATE order
                    SET calculated = 1  
                    WHERE user_id = {}
                    AND id = {}
                '''.format(user['id'], order['id'])
        try:
            result, ex = DatabaseHelper.execute(query)
            if (ex != None):
                return ex
            else:
                return None
        except Exception as ex:
            return ''' User {}-{}, Update-Order: {} '''.format(user['username'], user['id'], str(ex))
    # # --------------------------------------------------------------------------
    # # Update Order State
    # # --------------------------------------------------------------------------
    # def updateOrder(self, user, order):
    #     query = '''UPDATE order
    #                 set price = '{}', customer_name = '{}', customer_phone = '{}',
    #                     customer_email = '{}', address_shipping = '{}',
    #                     voucher_code = '{}', voucher_price = '{}',
    #                     delivery_info = '{}', payment_method = '{}',
    #                     remarks = '{}', gift_message = '{}', shipping_fee = '{}',
    #                     status = '{}', updated_at = '{}', order_json = '{}'
    #                 WHERE id = '{}'
    #             '''.format(order['price'], order['customer_name'], order['customer_phone'],
    #                        order['customer_email'], order['address_shipping'],
    #                        order['voucher_code'], order['voucher_price'],
    #                        order['delivery_info'], order['payment_method'],
    #                        order['remarks'], order['gift_message'], order['shipping_fee'],
    #                        order['status'], order['updated_at'], order['order_json'])
    #     try:
    #         DatabaseHelper.execute(query)
    #         return ExceptionUtils.success()
    #     except Exception as ex:
    #         return ExceptionUtils.error('''User: {}-{}, Order-Number: {}, Update-Order-State exception: {}'''.format(user['username'], user['id'], orderNumber, str(ex)))

    # # --------------------------------------------------------------------------
    # # Update Order State
    # # --------------------------------------------------------------------------
    # def updateOrderState(self, user, order):
    #     query = '''UPDATE order
    #                 set status = '{}', updated_at = '{}', order_json = '{}'
    #                 WHERE id = '{}'
    #             '''.format(order['status'], order['updated_at'], order['order_json'], order['id'])
    #     try:
    #         DatabaseHelper.execute(query)
    #         return ExceptionUtils.success()
    #     except Exception as ex:
    #         return ExceptionUtils.error('''User: {}-{}, Order-Number: {}, Update-Order-State exception: {}'''.format(user['username'], user['id'], orderNumber, str(ex)))








