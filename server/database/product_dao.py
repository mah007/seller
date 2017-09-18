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
                special_price       INTEGER         ,           # Only using for Prict-By-Time
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
                        brand, model, primary_category, spu_id, special_price,
                        user_id, quantity, original_price)
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}',
                            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                '''.format(product['name'], product['url'], product['status'],
                           product['seller_sku'], product['shop_sku'],
                           product['image'], product['package_width'],
                           product['package_height'], product['package_weight'],
                           product['brand'], product['model'],
                           product['primary_category'], product['spu_id'],
                           product['special_price'], user['id'], 0, 0)
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''Insert product exception: {}'''.format(str(ex)))

    # --------------------------------------------------------------------------
    # Get Product by seller SKU
    # --------------------------------------------------------------------------
    def getProductBySellerSku(self, user, sku):
        query = '''SELECT *
                    from product
                    WHERE user_id = '{}' and seller_sku = '{}'
                '''.format(user['id'], sku['sku'])
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            row = cur.fetchone()
            if not row:
                conn.close()
                errorMessage = '''User: {}-{}, Get-Product-By-SKU: {} is not found'''.format(user['username'], user['id'], sku['sku'])
                return None, errorMessage

            product = {
                    "id": row[0],
                    "name": row[1],
                    "url": row[2],
                    "status": row[3],
                    "quantity": row[4],
                    "seller_sku": row[5],
                    "shop_sku": row[6],
                    "original_price": row[7],
                    "special_price": row[8],
                    "image": row[9],
                    "width": row[10],
                    "height": row[11],
                    "weight": row[12],
                    "brand": row[13],
                    "model": row[14],
                    "primary_category": row[15],
                    "spu_id": row[16]
                }

            conn.close()
            return product, None
        except Exception as ex:
            errorMessage = '''Get-Product-By-SKU {}, exception: {}'''.format(sku, str(ex))
            return None, errorMessage


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
                    "seller_sku": row[5],
                    "shop_sku": row[6],
                    "original_price": row[7],
                    "special_price": row[8],
                    "image": row[9],
                    "width": row[10],
                    "height": row[11],
                    "weight": row[12],
                    "brand": row[13],
                    "model": row[14],
                    "primary_category": row[15],
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
                        spu_id = '{}', special_price = '{}'
                    WHERE shop_sku = '{}'
                '''.format(product['name'], product['url'], product['status'],
                           product['seller_sku'], product['image'],
                           product['package_width'], product['package_height'],
                           product['package_weight'], product['brand'],
                           product['model'], product['primary_category'],
                           product['spu_id'], product['special_price'],
                           product['shop_sku'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, update Product exception: {}'''.format(user['username'], user['id'], str(ex)))

    # --------------------------------------------------------------------------
    # Search Product by name, seller sku, shop sku, brand and model
    # --------------------------------------------------------------------------
    def searchProduct(self, user, searchKey):
        query = '''SELECT *
                    FROM product
                    WHERE (name LIKE '%{}%' OR seller_sku LIKE '%{}%'
                            OR shop_sku LIKE '%{}%' OR brand LIKE '%{}%'
                            OR model LIKE '%{}%') AND user_id = '{}'
                '''.format(searchKey, searchKey, searchKey, searchKey, searchKey, user['id'])
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
                    "seller_sku": row[5],
                    "shop_sku": row[6],
                    "original_price": row[7],
                    "special_price": row[8],
                    "image": row[9],
                    "width": row[10],
                    "height": row[11],
                    "weight": row[12],
                    "brand": row[13],
                    "model": row[14],
                    "primary_category": row[15],
                    "spu_id": row[16]
                })

            conn.close()
            return (products, None)
        except Exception as ex:
            return (None, ExceptionUtils.error('''Get products exception: {}'''.format(str(ex))))










