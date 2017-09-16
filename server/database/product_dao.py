from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.exception_utils import ExceptionUtils


class ProductDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS product(
                id                  INT AUTO_INCREMENT primary key NOT NULL,
                name                VARCHAR(150)    NOT NULL,
                url                 VARCHAR(250)    NOT NULL,
                status              VARCHAR(100)    NOT NULL,
                quantity            INTEGER         ,
                seller_sku          VARCHAR(100)    NOT NULL,
                shop_sku            VARCHAR(100)    NOT NULL,
                original_price      INTEGER         ,
                image               VARCHAR(250)    NOT NULL,   # Get first image from Lazada's product
                package_width       INTEGER         NOT NULL,
                package_height      INTEGER         NOT NULL,
                package_weight      INTEGER         NOT NULL,
                brand               VARCHAR(100)    NOT NULL,
                model               VARCHAR(100)    NOT NULL,
                primary_category    INTEGER         NOT NULL,
                spu_id              INTEGER         ,
                user_id             INTEGER         NOT NULL
                );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert Product
    # --------------------------------------------------------------------------
    def insert(self, user, product):
        query = '''INSERT INTO product(name, url, status, seller_sku, shop_sku,
                        image, package_width, package_height, package_weight,
                        brand, model, primary_category, spu_id, user_id,
                        quantity, original_price)
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}',
                            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                '''.format(product['name'], product['url'], product['status'],
                           product['seller_sku'], product['shop_sku'],
                           product['image'], product['package_width'],
                           product['package_height'], product['package_weight'],
                           product['brand'], product['model'],
                           product['primary_category'], product['spu_id'],
                           user['id'], 0, 0)
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''Insert product exception: {}'''.format(str(ex)))

    # --------------------------------------------------------------------------
    # Get All Product
    # --------------------------------------------------------------------------
    def getAllProduct(self, user):
        query = '''SELECT *
                    from product
                    WHERE user_id = '{}'
                    ORDER BY quantity, original_price
                    ASC LIMIT 30
                '''.format(user['id'])
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            products = []
            rows = cur.fetchall()
            for row in rows:
                products.append({
                    "id": row[0],
                    "name": row[1],
                    "url": row[2],
                    "status": row[3],
                    "quantity": row[4],
                    "sellerSku": row[5],
                    "shopSku": row[6],
                    "original_price": row[7],
                    "price": row[8],
                    "image": row[9],
                    "width": row[10],
                    "height": row[11],
                    "weight": row[12],
                    "branch": row[13],
                    "model": row[14],
                    "primaryCategory": row[15],
                    "spu_id": row[16]
                })

            conn.close()
            return products
        except Exception as ex:
            return ExceptionUtils.error('''Get products exception: {}'''.format(str(ex)))

    # --------------------------------------------------------------------------
    # Update Product (contain quantity and price)
    # --------------------------------------------------------------------------
    def updateProduct(self, product):
        query = '''UPDATE product
                    set quantity = '{}', original_price = '{}'
                    WHERE id = '{}'
                '''.format(product['quantity'], product['price'], product['id'])
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Update Product Quantity
    # --------------------------------------------------------------------------
    def updateProductQuantity(self, product):
        query = '''UPDATE product
                    set quantity = '{}'
                    WHERE id = '{}'
                '''.format(product['quantity'], product['id'])
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Update Product Price
    # --------------------------------------------------------------------------
    def updateProductPrice(self, product):
        query = '''UPDATE product
                    set original_price = '{}'
                    WHERE id = '{}'
                '''.format(product['price'], product['id'])
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Check Product exsits
    # --------------------------------------------------------------------------
    def isProductExist(self, user, shopSku):
        query = '''SELECT id
                    FROM product
                    WHERE shop_sku = '{}' AND user_id = '{}'
                '''.format(shopSku, user['id'])
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)
            product = cur.fetchone()
            result = False if not product else True;
            conn.close()
            return result, None
        except Exception as ex:
            errorString = '''User: {}-{}, Check-Product-Exist exception: {}'''.format(user['username'], user['id'], str(ex))
            return False, errorString

    # --------------------------------------------------------------------------
    # Update Product with Lazada Product
    # --------------------------------------------------------------------------
    def updateProductWithLazadaProduct(self, user, product):
        query = '''UPDATE product
                    set name = '{}', url = '{}', status = '{}', seller_sku = '{}',
                        image = '{}', package_width = '{}',
                        package_height = '{}', package_weight = '{}',
                        brand = '{}', model = '{}', primary_category = '{}',
                        spu_id = '{}', user_id = '{}'
                    WHERE shop_sku = '{}'
                '''.format(product['name'], product['url'], product['status'],
                           product['seller_sku'], product['image'],
                           product['package_width'], product['package_height'],
                           product['package_weight'], product['brand'],
                           product['model'], product['primary_category'],
                           product['spu_id'], user['id'],
                           product['shop_sku'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, update Product exception: {}'''.format(user['username'], user['id'], str(ex)))










