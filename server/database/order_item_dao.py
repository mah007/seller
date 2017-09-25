from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.exception_utils import ExceptionUtils


class OrderItemDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS order_item(
                id                      INT AUTO_INCREMENT primary key NOT NULL,
                order_item_id           BIGINT,
                shop_id                 VARCHAR(100),
                order_id                INTEGER,
                name                    VARCHAR(300),
                seller_sku              VARCHAR(300),
                shop_sku                VARCHAR(300),
                shipping_type           VARCHAR(100),
                item_price              DECIMAL(10,2),
                paid_price              DECIMAL(10,2),
                currency                VARCHAR(50),
                wallet_credit           INTEGER,
                tax_amount              INTEGER,
                shipping_amount         DECIMAL(10,2),
                shipping_service_cost   DECIMAL(10,2),
                voucher_amount          DECIMAL(10,2),
                voucher_code            VARCHAR(100),
                status                  VARCHAR(100),
                shipment_provider       VARCHAR(100),
                is_digital              INTEGER,
                digital_delivery_info   VARCHAR(300),
                tracking_code           VARCHAR(100),
                tracking_code_pre       VARCHAR(100),
                reason                  VARCHAR(300),
                reason_detail           TEXT,
                purchase_order_id       VARCHAR(100),
                purchase_order_number   VARCHAR(100),
                package_id              VARCHAR(100),
                promised_shipping_time  VARCHAR(100),
                extra_attributes        VARCHAR(300),
                shipping_provider_type  VARCHAR(100),
                created_at              DATETIME,
                updated_at              DATETIME,
                return_status           VARCHAR(300),
                product_main_image      VARCHAR(500),
                variation               VARCHAR(300),
                product_detail_url      VARCHAR(500),
                invoice_number          VARCHAR(100),
                user_id                 INTEGER
                );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert order
    # --------------------------------------------------------------------------
    def insert(self, user, orderItem):
        query = '''INSERT INTO order_item(order_item_id, shop_id, order_id, name,
                        seller_sku, shop_sku, shipping_type, item_price, paid_price,
                        currency, wallet_credit, tax_amount, shipping_service_cost,
                        voucher_amount, voucher_code, status, shipment_provider,
                        is_digital, digital_delivery_info, tracking_code, tracking_code_pre,
                        reason, reason_detail, purchase_order_id, purchase_order_number,
                        package_id, promised_shipping_time, extra_attributes,
                        shipping_provider_type, created_at, updated_at, return_status,
                        product_main_image, variation, product_detail_url, invoice_number,
                        user_id)
                    VALUES ('{}', '{}', '{}', "{}", "{}", '{}', '{}', '{}', '{}', '{}',
                            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}',
                            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}',
                            '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                '''.format(orderItem['order_item_id'], orderItem['shop_id'], orderItem['order_id'],
                           orderItem['name'], orderItem['seller_sku'], orderItem['shop_sku'],
                           orderItem['shipping_type'], orderItem['item_price'], orderItem['paid_price'],
                           orderItem['currency'], orderItem['wallet_credit'], orderItem['tax_amount'],
                           orderItem['shipping_service_cost'], orderItem['voucher_amount'], orderItem['voucher_code'],
                           orderItem['status'], orderItem['shipment_provider'], orderItem['is_digital'],
                           orderItem['digital_delivery_info'], orderItem['tracking_code'], orderItem['tracking_code_pre'],
                           orderItem['reason'], orderItem['reason_detail'], orderItem['purchase_order_id'],
                           orderItem['purchase_order_number'], orderItem['package_id'], orderItem['promised_shipping_time'],
                           orderItem['extra_attributes'], orderItem['shipping_provider_type'], orderItem['created_at'],
                           orderItem['updated_at'], orderItem['return_status'], orderItem['product_main_image'],
                           orderItem['variation'], orderItem['product_detail_url'], orderItem['invoice_number'],
                           user['id'])
        try:
            result, ex = DatabaseHelper.execute(query)
            if (result == True):
                return None, None
            else:
                return None, '''User: {}-{}, Insert-Order-Item: {}'''.format(user['username'], user['id'], str(ex))
        except Exception as ex:
            return '''User: {}-{}, Insert-Order: {}'''.format(user['username'], user['id'], str(ex))

    # --------------------------------------------------------------------------
    # Check Order exsits
    # --------------------------------------------------------------------------
    def isOrderItemExist(self, user, orderItemId):
        query = '''SELECT id FROM order_item WHERE order_item_id = '{}' AND user_id = '{}'
                '''.format(orderItemId, user['id'])
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)
            order = cur.fetchone()
            result = False if not order else True;
            conn.close()
            return result, None
        except Exception as ex:
            return False, '''User: {}-{}, Check-OrderItem-Exist: {}'''.format(user['username'], user['id'], str(ex))

    # --------------------------------------------------------------------------
    # Get order by order number
    # --------------------------------------------------------------------------
    def getOrderItemByOrderItemId(self, user, orderItemId):
        query = '''SELECT *
                    FROM order_item
                    WHERE user_id = '{}' AND order_item_id = '{}'
                '''.format(user['id'], orderNumber)
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            row = cur.fetchone()
            if not row:
                conn.close()
                return None, '''User: {}-{}, Get-Order-Item: {} is not found'''.format(user['username'], user['id'], orderItemId)

            orderItem = {
                'id': row[0],
                'order_item_id': row[1],
                'shop_id': row[2],
                'order_id': row[3],
                'name': row[4],
                'seller_sku': row[5],
                'shop_sku': row[6],
                'shipping_type': row[7],
                'item_price': row[8],
                'paid_price': row[9],
                'currency': row[10],
                'wallet_credit': row[11],
                'tax_amount': row[12],
                'shipping_service_cost': row[13],
                'voucher_amount': row[14],
                'voucher_code': row[15],
                'status': row[16],
                'shipment_provider': row[17],
                'is_digital': row[18],
                'digital_delivery_info': row[19],
                'tracking_code': row[20],
                'tracking_code_pre': row[21],
                'reason': row[22],
                'reason_detail': row[23],
                'purchase_order_id': row[24],
                'purchase_order_number': row[25],
                'package_id': row[26],
                'promised_shipping_time': row[27],
                'extra_attributes': row[28],
                'shipping_provider_type': row[29],
                'created_at': row[30],
                'updated_at': row[31],
                'return_status': row[32],
                'product_main_image': row[33],
                'variation': row[34],
                'product_detail_url': row[35],
                'invoice_number': row[36]
            }
            conn.close()
            return order, None
        except Exception as ex:
            return None, '''User: {}-{}, Order-Number: {}, Get-Order-By-Order-Number exception {}'''.format(user['username'], user['id'], orderNumber, str(ex))

    # --------------------------------------------------------------------------
    # Update Order State
    # --------------------------------------------------------------------------
    def deleteOrderItemByOrderId(self, user, orderId):
        query = '''DELETE from order_item WHERE order_id = '{}' and user_id = '{}'
                '''.format(orderId, user['id'])
        try:
            result, ex = DatabaseHelper.execute(query)
            if (ex != None):
                return False, ex
            else:
                return True, None
        except Exception as ex:
            return False, '''User: {}-{}, Delete-Order-Items: {}'''.format(user['username'], user['id'], str(ex))








