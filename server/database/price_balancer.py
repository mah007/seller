import psycopg2
from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils

# ------------------------------------------------------------------------------
# TODO: Handle exception
# ------------------------------------------------------------------------------

class PriceBalancerDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS price_balancer(
                    id              INT AUTO_INCREMENT primary key NOT NULL,
                    sku             VARCHAR(200)     	NOT NULL,
                    name            TEXT                NOT NULL,
                    url             TEXT                NOT NULL,
                    current_price    INT                 NOT NULL,
                    price_by_time   INT
                    );'''
        DatabaseHelper.execute(query)


    def insert(self, pb):
        query = '''INSERT INTO price_balancer (sku, name, url, current_price, price_by_time)
                    VALUES ('{}', '{}', '{}', '{}', '{}')'''.format(
                    StringUtils.toString(pb['sku']),
                    StringUtils.toString(pb['name']),
                    StringUtils.toString(pb['url']),
                    StringUtils.toString(pb['current_price']),
                    StringUtils.toString(pb['price_by_time']))
        DatabaseHelper.execute(query)


    def getPriceBalancer(self, id):
        try:
            query = '''SELECT * FROM price_balancer WHERE id='{}' '''.format(id)
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            rows = cur.fetchall()
            if not rows:
                conn.close()
                return None

            prices = {}
            for row in rows:
                prices['sku'] = row[1]
                prices['name'] = row[2]  
                prices['url'] = row[3]
                prices['current_price'] = row[4]
                prices['price_by_time'] = row[5]

            conn.close()
            return prices
        except Exception as ex:
            print(ex)
            return None





