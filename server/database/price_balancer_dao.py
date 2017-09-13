from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.exception_utils import ExceptionUtils

class PriceBalancerDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS price_balancer(
                    id              INT AUTO_INCREMENT primary key NOT NULL,
                    sku             VARCHAR(100)        NOT NULL,
                    name            VARCHAR(300)        NOT NULL,
                    link            VARCHAR(300)        NOT NULL,
                    price_balance   VARCHAR(300)        NOT NULL,
                    user_id         INTEGER             NOT NULL
                    );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert price balancer
    # --------------------------------------------------------------------------
    def insert(self, sku, user):
        query = '''INSERT INTO price_balancer(sku, name, link, price_balance, user_id)
                    VALUES ('{}', '{}', '{}', '{}', '{}')'''.format(
                    StringUtils.toString(sku['sku']), StringUtils.toString(sku['name']),
                    StringUtils.toString(sku['link']), sku['price_balance'], user['id'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, Insert price balancer exception: {}'''.format(user['username'], user['id'], str(ex)))

    # --------------------------------------------------------------------------
    # Update price balancer
    # --------------------------------------------------------------------------
    def update(self, sku, user):
        query = '''UPDATE price_balancer
                    set price_balance = '{}'
                    WHERE id = '{}'
                '''.format(sku['price_balance'], sku['id'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, update price balancer: {}, exception: {}'''.format(user['username'], user['id'], sku['id'], str(ex)))

    # --------------------------------------------------------------------------
    # Delete price balancer
    # --------------------------------------------------------------------------
    def delete(self, sku, user):
        query = '''DELETE from price_balancer where id = '{}' '''.format(sku['id'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, delete price balancer: {}, exception: {}'''.format(user['username'], user['id'], sku['id'], str(ex)))

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
                    "link": row[3],
                    "price_balance": row[4],
                })

            conn.close()
            return skus
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, get balancer skus exception: {}'''.format(user['username'], user['id'], str(ex)))


















