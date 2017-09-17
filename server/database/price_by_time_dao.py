from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.exception_utils import ExceptionUtils

class PriceByTimeDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS price_by_time(
                    id              INT AUTO_INCREMENT primary key NOT NULL,
                    sku             VARCHAR(100)        NOT NULL,
                    name            VARCHAR(300)        ,
                    link            VARCHAR(300)        ,
                    price_by_time   VARCHAR(300)        ,
                    special_price   INTEGER             ,
                    user_id         INTEGER             NOT NULL
                    );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert price by time
    # --------------------------------------------------------------------------
    def insert(self, sku, user):
        query = '''INSERT INTO price_by_time(sku, name, link, price_by_time, special_price, user_id)
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}')'''.format(
                    StringUtils.toString(sku['sku']), StringUtils.toString(sku['name']),
                    StringUtils.toString(sku['link']), sku['price_by_time'],
                    sku['special_price'], user['id'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, Insert price by time exception: {}'''.format(user['username'], user['id'], str(ex)))

    # --------------------------------------------------------------------------
    # Update price by time
    # --------------------------------------------------------------------------
    def update(self, sku, user):
        query = '''UPDATE price_by_time
                    set price_by_time = '{}'
                    WHERE id = '{}'
                '''.format(sku['price_by_time'], sku['id'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, update sku: {}, exception: {}'''.format(user['username'], user['id'], sku['id'], str(ex)))

    def updateSpecialPrice(self, sku, user, newSpecialPrice):
        query = '''UPDATE price_by_time
                    set special_price = '{}'
                    WHERE id = '{}'
                '''.format(newSpecialPrice, sku['id'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, update special price of sku: {}, exception: {}'''.format(user['username'], user['id'], sku['id'], str(ex)))

    # --------------------------------------------------------------------------
    # Delete price by time
    # --------------------------------------------------------------------------
    def delete(self, sku, user):
        query = '''DELETE from price_by_time where id = '{}' '''.format(sku['id'])
        try:
            DatabaseHelper.execute(query)
            return ExceptionUtils.success()
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, delete price by time: {}, exception: {}'''.format(user['username'], user['id'], sku['id'], str(ex)))

    # --------------------------------------------------------------------------
    # get price by times
    # --------------------------------------------------------------------------
    def getAll(self, user):
        query = '''SELECT * from price_by_time WHERE user_id = '{}'
                '''.format(user['id'])
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
                    "price_by_time": row[4],
                    "special_price": row[5]
                })

            conn.close()
            return skus
        except Exception as ex:
            return ExceptionUtils.error('''User: {}-{}, get by time skus exception: {}'''.format(user['username'], user['id'], str(ex)))


















