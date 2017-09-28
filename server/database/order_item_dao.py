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
                user_id                 INTEGER,
                earned                  INTEGER DEFAULT 0
                );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert order
    # --------------------------------------------------------------------------
    def insert(self, user, orderItem):
        query = '''INSERT INTO order_item(order_item_id, shop_id, order_id, name,
                        seller_sku, shop_sku, shipping_type, item_price, paid_price,
                        currency, wallet_credit, tax_amount, shipping_service_cost,
                        shipping_amount, voucher_amount, voucher_code, status, shipment_provider,
                        is_digital, digital_delivery_info, tracking_code, tracking_code_pre,
                        reason, reason_detail, purchase_order_id, purchase_order_number,
                        package_id, promised_shipping_time, extra_attributes,
                        shipping_provider_type, created_at, updated_at, return_status,
                        product_main_image, variation, product_detail_url, invoice_number,
                        user_id)
                    VALUES ('{}', '{}', '{}', "{}", "{}", '{}', '{}', '{}', '{}', '{}',
                            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}',
                            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}',
                            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
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
    # Get OrderItem by OrderId
    # --------------------------------------------------------------------------
    def getOrderItemByOrderId(self, user, orderId):
        query = '''SELECT *
                    FROM order_item
                    WHERE user_id = '{}' AND order_id = '{}'
                '''.format(user['id'], orderId)
        return self.getOrderItems(user, query)

    # --------------------------------------------------------------------------
    # Get OrderItem by OrderItemId
    # --------------------------------------------------------------------------
    def getOrderItemByOrderItemId(self, user, orderItemId):
        query = '''SELECT *
                    FROM order_item
                    WHERE user_id = '{}' AND order_item_id = '{}'
                '''.format(user['id'], orderItemId)
        return self.getOrderItems(user, query)

    def getOrderItemByShopSku(self, user, shopSku):
        query = ''' SELECT *
                    FROM order_item
                    WHERE user_id = '{}' AND shop_sku = '{}' AND earned = 0
                '''.format(user['id'], shopSku)
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchone()
            orderItem = []
            for row in rows:
                orderItem.append({
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
                        'shipping_amount': row[13],
                        'shipping_service_cost': row[14],
                        'voucher_amount': row[15],
                        'voucher_code': row[16],
                        'status': row[17],
                        'shipment_provider': row[18],
                        'is_digital': row[19],
                        'digital_delivery_info': row[20],
                        'tracking_code': row[21],
                        'tracking_code_pre': row[22],
                        'reason': row[23],
                        'reason_detail': row[24],
                        'purchase_order_id': row[25],
                        'purchase_order_number': row[26],
                        'package_id': row[27],
                        'promised_shipping_time': row[28],
                        'extra_attributes': row[29],
                        'shipping_provider_type': row[30],
                        'created_at': row[31],
                        'updated_at': row[32],
                        'return_status': row[33],
                        'product_main_image': row[34],
                        'variation': row[35],
                        'product_detail_url': row[36],
                        'invoice_number': row[37]
                    })
                conn.close()
                return orderItem, None
        except Exception as ex:
            return None, '''User: {}-{}, Query: {}, Get-Order-By-Order-Number exception {}'''.format(user['username'], user['id'], query, str(ex))

    def getOrderItems(self, user, query):
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            orderItems = []
            rows = cur.fetchall()
            for row in rows:
                orderItems.append({
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
                    'shipping_amount': row[13],
                    'shipping_service_cost': row[14],
                    'voucher_amount': row[15],
                    'voucher_code': row[16],
                    'status': row[17],
                    'shipment_provider': row[18],
                    'is_digital': row[19],
                    'digital_delivery_info': row[20],
                    'tracking_code': row[21],
                    'tracking_code_pre': row[22],
                    'reason': row[23],
                    'reason_detail': row[24],
                    'purchase_order_id': row[25],
                    'purchase_order_number': row[26],
                    'package_id': row[27],
                    'promised_shipping_time': row[28],
                    'extra_attributes': row[29],
                    'shipping_provider_type': row[30],
                    'created_at': row[31],
                    'updated_at': row[32],
                    'return_status': row[33],
                    'product_main_image': row[34],
                    'variation': row[35],
                    'product_detail_url': row[36],
                    'invoice_number': row[37]
                })
            conn.close()
            return orderItems, None
        except Exception as ex:
            return None, '''User: {}-{}, Query: {}, Get-Order-By-Order-Number exception {}'''.format(user['username'], user['id'], query, str(ex))

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

    def setEarned(self, user, item):
        query = ''' UPDATE order_item 
                    SET earned = 1  
                    WHERE user_id = {}
                    AND id = {}
                '''.format(user['id'], item['id'])
        try:
            result, ex = DatabaseHelper.execute(query)
            if (ex != None):
                return ex
            else:
                return None
        except Exception as ex:
            return ''' User {}-{}, Update-Order-Items: {} '''.format(user['username'], user['id'], str(ex))








