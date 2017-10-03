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
                earned                  DECIMAL(10,2) DEFAULT 0,
                purchase_price          DECIMAL(10,2) DEFAULT 0
                );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert OrderItem
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
                           orderItem['shipping_service_cost'], orderItem['shipping_amount'],
                           orderItem['voucher_amount'], orderItem['voucher_code'],
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
            return '''User: {}-{}, Insert-Order-Item: {}'''.format(user['username'], user['id'], str(ex))

    # --------------------------------------------------------------------------
    # Update OrderItem
    # --------------------------------------------------------------------------
    def update(self, user, orderItem):
        query = '''UPDATE order_item
                    SET shop_id = %s, name = %s, seller_sku = %s, shop_sku = %s,
                        shipping_type = %s, item_price = %s, paid_price = %s,
                        currency = %s, wallet_credit = %s, tax_amount = %s,
                        shipping_service_cost = %s, shipping_amount = %s,
                        voucher_amount = %s, voucher_code = %s, status = %s,
                        shipment_provider = %s, is_digital = %s,
                        digital_delivery_info = %s, tracking_code = %s,
                        tracking_code_pre = %s, reason = %s, reason_detail = %s,
                        purchase_order_id = %s, purchase_order_number = %s,
                        package_id = %s, promised_shipping_time = %s,
                        extra_attributes = %s, shipping_provider_type = %s,
                        created_at = %s, updated_at = %s, return_status = %s,
                        product_main_image = %s, variation = %s,
                        product_detail_url = %s, invoice_number = %s
                    WHERE user_id = %s AND order_item_id = %s'''

        conn = DatabaseHelper.getConnection()
        cur = conn.cursor()
        try:
            cur.execute(query, (orderItem['shop_id'], orderItem['name'], orderItem['seller_sku'],
                                orderItem['shop_sku'], orderItem['shipping_type'],
                                orderItem['item_price'], orderItem['paid_price'],
                                orderItem['currency'], orderItem['wallet_credit'],
                                orderItem['tax_amount'], orderItem['shipping_service_cost'],
                                orderItem['shipping_amount'], orderItem['voucher_amount'],
                                orderItem['voucher_code'], orderItem['status'],
                                orderItem['shipment_provider'], orderItem['is_digital'],
                                orderItem['digital_delivery_info'], orderItem['tracking_code'],
                                orderItem['tracking_code_pre'], orderItem['reason'],
                                orderItem['reason_detail'], orderItem['purchase_order_id'],
                                orderItem['purchase_order_number'], orderItem['package_id'],
                                orderItem['promised_shipping_time'], orderItem['extra_attributes'],
                                orderItem['shipping_provider_type'], orderItem['created_at'],
                                orderItem['updated_at'], orderItem['return_status'],
                                orderItem['product_main_image'], orderItem['variation'],
                                orderItem['product_detail_url'], orderItem['invoice_number'],
                                user['id'], orderItem['order_item_id']))
            conn.commit()
            conn.close()
            return None, None
        except Exception as ex:
            conn.rollback()
            conn.close()
            return None, '''User: {}-{}, Update-Order-Item: {}, Query: {}'''.format(user['username'], user['id'], str(ex), query)

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

    # --------------------------------------------------------------------------
    # Get OrderItem by OrderId and ShopSku
    # --------------------------------------------------------------------------
    def getOrderItemByShopSku(self, user, orderId, shopSku):
        query = ''' SELECT *
                    FROM order_item
                    WHERE order_id = {} AND user_id = '{}' AND shop_sku = '{}'
                '''.format(orderId, user['id'], shopSku)
        return self.getOrderItems(user, query)

    # --------------------------------------------------------------------------
    # Get OrderItem by query for thoese functions above
    # --------------------------------------------------------------------------
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
                    'invoice_number': row[37],
                    'earned': row[39], # row[38] is user_id, don't need it
                    'purchase_price': row[40]
                })
            conn.close()
            return orderItems, None
        except Exception as ex:
            return None, '''User: {}-{}, Query: {}, Get-Order-Item-By-Order-Item-Id: {}'''.format(user['username'], user['id'], query, str(ex))

    # --------------------------------------------------------------------------
    # Delete OrderItem by order id
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

    # --------------------------------------------------------------------------
    # Set Income for an OrderItem
    # --------------------------------------------------------------------------
    def setIncome(self, user, orderId, shopSku, income):
        query = ''' UPDATE order_item
                    SET earned = {}
                    WHERE order_id = {} AND user_id = '{}' AND shop_sku = '{}'
                '''.format(income, orderId, user['id'], shopSku)
        try:
            result, exception = DatabaseHelper.execute(query)
            return exception # Exception will be null if not have any exception
        except Exception as ex:
            return '''User {}-{}, Set-Order-Item-Income: Order-Item-Id {}, Exception: {} '''.format(user['username'], user['id'], itemItemId, str(ex))

    # --------------------------------------------------------------------------
    # Mark order that is calculated for an Account Statement
    # --------------------------------------------------------------------------
    def getOrderItemByAccountStatement(self, user, accountStatementId):
        query = '''SELECT order.order_id, order_item.order_item_id, order.order_number,
                        order_item.name, order_item.seller_sku, order_item.product_main_image,
                        order_item.item_price, order_item.purchase_price, order_item.earned,
                        order_item.shop_sku
                    FROM `order`
                    INNER JOIN `order_item` ON order.order_id = order_item.order_id
                    WHERE order.user_id = {} AND order.account_statement_id = {}
                    LIMIT 10
                '''.format(user['id'], accountStatementId)
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            orderItems = []
            rows = cur.fetchall()
            for row in rows:
                orderItems.append({
                    "order_id": row[0],
                    "order_item_id": row[1],
                    "order_number": row[2],
                    "name": row[3],
                    "seller_sku": row[4],
                    "product_main_image": row[5],
                    "item_price": row[6],
                    "purchase_price": row[7],
                    "earned": row[8],
                    "shop_sku": row[9]
                })
            conn.close()
            return orderItems, None
        except Exception as ex:
            return None, '''User: {}-{}, GetOrderItemByAccountStatement: {} '''.format(user['username'], user['id'], str(ex))







