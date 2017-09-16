from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.exception_utils import ExceptionUtils


class ProductDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS product(
                id                  INT AUTO_INCREMENT primary key NOT NULL,
                name                VARCHAR(80)     NOT NULL,
                url                 VARCHAR(150)    NOT NULL,
                status              VARCHAR(50)     NOT NULL,
                quantity            INTEGER         ,
                seller_sku          VARCHAR(50)     NOT NULL,
                shop_sku            VARCHAR(50)     NOT NULL,
                original_price      INTEGER         ,
                image               TEXT            NOT NULL,
                package_width       INTEGER         NOT NULL,
                package_height      INTEGER         NOT NULL,
                package_weight      INTEGER         NOT NULL,
                brand               VARCHAR(50)     NOT NULL,
                model               VARCHAR(50)     NOT NULL,
                primary_category    INTEGER         NOT NULL,
                created_time        VARCHAR(30)     NOT NULL,   # Lazada created time
                sku_id              INTEGER         NOT NULL,
                user_id             INTEGER         NOT NULL
                );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert Product
    # --------------------------------------------------------------------------
    def insert(self, product, user):
        try:
            query = '''INSERT INTO product(
                            name, url, status, sellerSku, shopSku, image,
                            width, height, weight, brand, model, primaryCategory,
                            user_id, quantity, original_price)
                        VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}')
                    '''.format(product['Attributes']['name'], product['Skus'][0]['Url'],
                                product['Skus'][0]['Status'], product['Skus'][0]['SellerSku'],
                                product['Skus'][0]['ShopSku'], product['Skus'][0]['Images'][0],
                                product['Skus'][0]['package_width'], product['Skus'][0]['package_height'],
                                product['Skus'][0]['package_weight'], product['Attributes']['brand'],
                                product['Attributes']['model'], product['PrimaryCategory'], user['id'], 0, 0)
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''Insert product failed: {}'''.format(str(ex)))

    # --------------------------------------------------------------------------
    # Get All Product
    # --------------------------------------------------------------------------
    def getAllProduct(self, user):
        try:
            query = '''SELECT * from product WHERE user_id = '{}' ORDER BY quantity, original_price ASC LIMIT 30 '''.format(user['id'])
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
                    "price": row[7],
                    "image": row[8],
                    "width": row[9],
                    "height": row[10],
                    "weight": row[11],
                    "branch": row[12],
                    "model": row[13],
                    "primaryCategory": row[14],
                })

            conn.close()
            return products
        except Exception as ex:
            return None

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








