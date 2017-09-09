from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.exception_utils import ExceptionUtils


class ProductDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS product(
                id              INT AUTO_INCREMENT primary key NOT NULL,
                name            VARCHAR(50)     NOT NULL,
                url             VARCHAR(50)     NOT NULL,
                status          TEXT            NOT NULL,
                quantity        INT,
                sellerSku       VARCHAR(50)     NOT NULL,
                shopSku         VARCHAR(50)     NOT NULL,
                original_price  INT,
                image           TEXT            NOT NULL,
                width           INT             NOT NULL,
                height          INT             NOT NULL,
                weight          INT             NOT NULL,
                brand          VARCHAR(50)     NOT NULL,
                model           VARCHAR(50)     NOT NULL,
                primaryCategory VARCHAR(50)     NOT NULL,
                user_id         INT             NOT NULL
                );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert Product
    # --------------------------------------------------------------------------
    def insert(self, product, user):
        print("Inserting")
        try:
            query = '''INSERT INTO product(name, url, status, sellerSku, shopSku, image,
                width, height, weight, brand, model, primaryCategory, user_id) VALUES ('{}', '{}', '{}', '{}', '{}',
                '{}', '{}', '{}', '{}', '{}','{}', '{}', '{}')'''.format(product['Attributes']['name'], 
                product['Skus']['Url'], product['Skus']['Status'], product['Skus']['SellerSku'], 
                product['Skus']['ShopSku'], product['Skus']['Images'], product['Skus']['package_width'], 
                product['Skus']['package_height'], product['Skus']['package_weight'], product['Attributes']['brand'], 
                product['Attributes']['model'], product['PrimaryCategory'], user['id'])
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''Insert product failed: {}'''.format(str(ex)))


    # --------------------------------------------------------------------------
    # Get All Product
    # --------------------------------------------------------------------------
    def getAllProduct(self, user):
        try:
            query = '''SELECT * from product WHERE user_id = '{}' ORDER BY id DESC LIMIT 30 '''.format(user['id'])
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
                    "sellerSku": row[5],
                    "shopSku": row[6],
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
            print(ex)
            return None








