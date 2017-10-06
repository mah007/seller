from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.exception_utils import ExceptionUtils

# ------------------------------------------------------------------------------
GET_PRODUCT_LIMIT = 10


class ProductDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS product(
                id                  INT AUTO_INCREMENT primary key NOT NULL,
                name                VARCHAR(150)    NOT NULL,
                url                 VARCHAR(250)    NOT NULL,
                status              VARCHAR(100)    NOT NULL,
                quantity            INTEGER         ,
                available_quantity  INTEGER         ,
                seller_sku          VARCHAR(100)    NOT NULL,
                shop_sku            VARCHAR(100)    NOT NULL,
                original_price      DECIMAL(10,2),
                special_price       DECIMAL(10,2),              # Only using for Prict-By-Time
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
                        user_id, available_quantity, quantity, original_price)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        conn = DatabaseHelper.getConnection()
        cur = conn.cursor()
        try:
            cur.execute(query, (product['name'], product['url'], product['status'],
                           product['seller_sku'], product['shop_sku'],
                           product['image'], product['package_width'],
                           product['package_height'], product['package_weight'],
                           product['brand'], product['model'],
                           product['primary_category'], product['spu_id'],
                           product['special_price'], user['id'], 0, 0, 0))
            conn.commit()
            conn.close()
            return None
        except Exception as ex:
            conn.rollback()
            conn.close()
            return '''Insert product exception: {}'''.format(str(ex))

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
                    "available_quantity": row[5],
                    "seller_sku": row[6],
                    "shop_sku": row[7],
                    "original_price": row[8],
                    "special_price": row[9],
                    "image": row[10],
                    "width": row[11],
                    "height": row[12],
                    "weight": row[13],
                    "brand": row[14],
                    "model": row[15],
                    "primary_category": row[16],
                    "spu_id": row[17]
                }

            conn.close()
            return product, None
        except Exception as ex:
            errorMessage = '''Get-Product-By-SKU {}, exception: {}'''.format(sku, str(ex))
            return None, errorMessage

    # --------------------------------------------------------------------------
    # Get Product by shop SKU
    # --------------------------------------------------------------------------
    def getProductByShopSku(self, user, shopSku):
        query = '''SELECT *
                    FROM product
                    WHERE user_id = '{}' and shop_sku = '{}'
                '''.format(user['id'], shopSku)
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            row = cur.fetchone()
            if not row:
                conn.close()
                errorMessage = '''User: {}-{}, Get-Product-By-SKU: {} is not found'''.format(user['username'], user['id'], shopSku)
                return None, errorMessage

            product = {
                    "id": row[0],
                    "name": row[1],
                    "url": row[2],
                    "status": row[3],
                    "quantity": row[4],
                    "available_quantity": row[5],
                    "seller_sku": row[6],
                    "shop_sku": row[7],
                    "original_price": row[8],
                    "special_price": row[9],
                    "image": row[10],
                    "width": row[11],
                    "height": row[12],
                    "weight": row[13],
                    "brand": row[14],
                    "model": row[15],
                    "primary_category": row[16],
                    "spu_id": row[17]
                }

            conn.close()
            return product, None
        except Exception as ex:
            errorMessage = '''Get-Product-By-SKU {}, exception: {}'''.format(shopSku, str(ex))
            return None, errorMessage

    # --------------------------------------------------------------------------
    # Get All Product
    # TODO: Need to refactor
    # --------------------------------------------------------------------------
    def getProducts(self, user):
        query = '''SELECT *
                    from product
                    WHERE user_id = '{}'
                    ORDER BY quantity, original_price
                    ASC LIMIT {}
                '''.format(user['id'], GET_PRODUCT_LIMIT)
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
                    "available_quantity": row[5],
                    "seller_sku": row[6],
                    "shop_sku": row[7],
                    "original_price": row[8],
                    "special_price": row[9],
                    "image": row[10],
                    "width": row[11],
                    "height": row[12],
                    "weight": row[13],
                    "brand": row[14],
                    "model": row[15],
                    "primary_category": row[16],
                    "spu_id": row[17]
                })

            conn.close()
            return products
        except Exception as ex:
            return ExceptionUtils.error('''Get products exception: {}'''.format(str(ex)))

    # --------------------------------------------------------------------------
    # Update Product (contain quantity and price)
    # TODO: need to refactor
    # --------------------------------------------------------------------------
    def updateProduct(self, product):
        query = '''UPDATE product
                    set quantity = '{}', original_price = '{}'
                    WHERE id = '{}'
                '''.format(product['quantity'], product['price'], product['id'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''Update product got exception: {}'''.format(str(ex)))

    # --------------------------------------------------------------------------
    # Update Product Quantity
    # TODO: need to refactor
    # --------------------------------------------------------------------------
    def updateProductQuantity(self, product):
        query = '''UPDATE product
                    set quantity = '{}'
                    WHERE id = '{}'
                '''.format(product['quantity'], product['id'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''Update product's quantity got exception: {}'''.format(str(ex)))

    # --------------------------------------------------------------------------
    # Update Product Price
    # TODO: need to refactor
    # --------------------------------------------------------------------------
    def updateProductPrice(self, product):
        query = '''UPDATE product
                    set original_price = '{}'
                    WHERE id = '{}'
                '''.format(product['price'], product['id'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''Update product's price got exception: {}'''.format(str(ex)))

    def updateOriginalPriceByShopSku(self, user, shopSku, orginalPrice):
        query = '''UPDATE product
                    set original_price = '{}'
                    WHERE shop_sku = '{}' AND user_id = '{}'
                '''.format(orginalPrice, shopSku, user['id'])
        try:
            result, exception = DatabaseHelper.execute(query)
            return exception
        except Exception as ex:
            return '''Update product's price got exception: {}'''.format(str(ex))


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
                    set name = %s, url = %s, status = %s, seller_sku = %s,
                        image = %s, package_width = %s,
                        package_height = %s, package_weight = %s,
                        brand = %s, model = %s, primary_category = %s,
                        spu_id = %s, special_price = %s
                    WHERE shop_sku = %s '''
        conn = DatabaseHelper.getConnection()
        cur = conn.cursor()
        try:
            cur.execute(query, (product['name'], product['url'], product['status'],
                           product['seller_sku'], product['image'],
                           product['package_width'], product['package_height'],
                           product['package_weight'], product['brand'],
                           product['model'], product['primary_category'],
                           product['spu_id'], product['special_price'],
                           product['shop_sku']))
            conn.commit()
            conn.close()
            return None
        except Exception as ex:
            conn.rollback()
            conn.close()
            return '''User: {}-{}, update Product exception: {}'''.format(user['username'], user['id'], str(ex))

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
                    "available_quantity": row[5],
                    "seller_sku": row[6],
                    "shop_sku": row[7],
                    "original_price": row[8],
                    "special_price": row[9],
                    "image": row[10],
                    "width": row[11],
                    "height": row[12],
                    "weight": row[13],
                    "brand": row[14],
                    "model": row[15],
                    "primary_category": row[16],
                    "spu_id": row[17]
                })

            conn.close()
            return (products, None)
        except Exception as ex:
            return (None, ExceptionUtils.error('''Get products exception: {}'''.format(str(ex))))









