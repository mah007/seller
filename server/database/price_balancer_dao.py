from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.exception_utils import ExceptionUtils

class PriceBalancerDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS price_balancer(
                    id              INT AUTO_INCREMENT primary key NOT NULL,
                    sku             VARCHAR(100)        NOT NULL,
                    name            VARCHAR(300)        NOT NULL,
                    url             VARCHAR(300)        NOT NULL,
                    current_price   INT                 NOT NULL,
                    price_by_time   INT                 NOT NULL,
                    user_id         INT                 NOT NULL
                    );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert price balancer
    # --------------------------------------------------------------------------
    def insert(self, pb, user):
        query = '''INSERT INTO price_balancer(sku, name, url, current_price, price_by_time, user_id)
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}')'''.format(
                    StringUtils.toString(pb['sku']), StringUtils.toString(pb['name']),
                    StringUtils.toString(pb['url']), pb['current_price'], pb['price_by_time'], user['id'])
        try:
            print(query)
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''Insert price balancer exception: {}'''.format(str(ex)))

    # --------------------------------------------------------------------------
    # Delete price balancer
    # --------------------------------------------------------------------------
    def delete(self, pb):
        query = '''DELETE from price_balancer where id = '{}' '''.format(pb['id'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''Delete price balancer: {}, exception: {}'''.format(pb['id'], str(ex)))

    # --------------------------------------------------------------------------
    # get price balancers
    # --------------------------------------------------------------------------
    def getAll(self, user):
        query = '''SELECT * from price_balancer WHERE user_id = '{}' '''.format(user['id'])
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            skus = []
            rows = cur.fetchall()
            for row in rows:
                skus.append({
                    "id": row[0],
                    "sku": row[1],
                    "name": row[2],
                    "url": row[3],
                    "current_price": row[4],
                    "price_by_time": row[5]
                })

            conn.close()
            return skus
        except Exception as ex:
            print(ex)
            return ExceptionUtils.error('''Get price balancer exception: {}'''.format(str(ex)))


















