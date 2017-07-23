from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils


class SkuDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS sku_management(
        			id 				INT AUTO_INCREMENT primary key NOT NULL,
                    sku           	VARCHAR(500)    	NOT NULL,
                    name          	VARCHAR(500)     	NOT NULL,
                    link			VARCHAR(500)		NOT NULL,
                    min_price     	INTEGER		NOT NULL,
                    max_price     	INTEGER    	NOT NULL,
                    compete_price 	INTEGER 	NOT NULL,
                    special_price   INTEGER     NOT NULL,
                    state			INTEGER		NOT NULL,
                    repeat_time 	INTEGER 	NOT NULL,
                    created_at 		INTEGER 	NOT NULL,
                    updated_at		INTEGER,
                    user_id          INTEGER     NOT NULL
                    );'''
        DatabaseHelper.execute(query)


    def getAll(self, user):
        try:
            query = '''SELECT * from sku_management WHERE user_id = '{}' ORDER BY id DESC LIMIT 100'''.format(user['id'])
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
                    "min_price": row[4],
                    "max_price": row[5],
                    "compete_price": row[6],
                    "special_price": row[7],
                    "state": row[8],
                    "repeat_time": row[9],
                    "created_at": row[10]
                })

            conn.close()
            return skus
        except Exception as ex:
            print(ex)
            return None

    # --------------------------------------------------------------------------
    # Get all active SKU of a user
    # --------------------------------------------------------------------------
    def getActiveSku(self, user):
        try:
            query = '''SELECT * from sku_management WHERE state = 1 and user_id = {} ORDER BY id DESC LIMIT 100'''.format(user['id'])
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
                    "min_price": row[4],
                    "max_price": row[5],
                    "compete_price": row[6],
                    "special_price": row[7],
                    "state": row[8],
                    "repeat_time": row[9],
                    "created_at": row[10]
                })

            conn.close()
            return skus
        except Exception as ex:
            print(ex)
            return None


    # --------------------------------------------------------------------------
    # Delete KSU
    # --------------------------------------------------------------------------
    def delete(self, sku):
        query = '''DELETE from sku_management where id = '{}' '''.format(sku['id'])
        DatabaseHelper.execute(query)


    # --------------------------------------------------------------------------
    # Insert KSU
    # --------------------------------------------------------------------------
    def insert(self, sku, user):
        query = '''INSERT INTO sku_management (sku, name, link, min_price, max_price,
    				compete_price, special_price, state, repeat_time, created_at, updated_at, user_id)
    				VALUES ('{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, 0, {})'''.format(
    				StringUtils.toString(sku['sku']), StringUtils.toString(sku['name']), StringUtils.toString(sku['link']),
                    sku['min_price'], sku['max_price'], sku['compete_price'], sku['special_price'], sku['state'], sku['repeat_time'], sku['created_at'],
                    user['id'])
        DatabaseHelper.execute(query)


    # ---------------------------------------------------------------------------------------
    # Update KSU
    # ---------------------------------------------------------------------------------------
    def update(self, sku):
        query = '''UPDATE sku_management set min_price = '{}', max_price = '{}', compete_price = '{}', updated_at = '{}'
                    WHERE id = '{}' '''.format(sku['min_price'], sku['max_price'], sku['compete_price'],
                    sku['updated_at'], sku['id'])
        DatabaseHelper.execute(query)


    # ---------------------------------------------------------------------------------------
    # [pRunner] Update Specical Price
    # ---------------------------------------------------------------------------------------
    def updateSpecialPrice(self, sku):
        query = '''UPDATE sku_management set special_price = '{}' WHERE id = '{}' '''.format(sku['special_price'], sku['id'])
        DatabaseHelper.execute(query)


    # ---------------------------------------------------------------------------------------
    # Update KSU
    # ---------------------------------------------------------------------------------------
    def updateState(self, sku):
        query = '''UPDATE sku_management set state = {} WHERE id = '{}' '''.format(sku['state'], sku['id'])
        DatabaseHelper.execute(query)
        
    def getAddedSize(self, username):
        query = ''' SELECT count(*) FROM sku_management as sku, t_user as user  WHERE user.id = sku.user_id AND user.lazada_user_name = '{}'  '''.format(StringUtils.toString(username))
        conn = DatabaseHelper.getConnection()
        cur = conn.cursor()
        cur.execute(query)

        count = 0
        row = cur.fetchone()
        count = row[0];

        conn.close()
        return count


    def getCertainSize(self, username):        
        query = ''' SELECT certain_size FROM t_user WHERE lazada_user_name = '{}' '''.format(StringUtils.toString(username))
        conn = DatabaseHelper.getConnection()
        cur = conn.cursor()
        cur.execute(query)

        count = 0
        row = cur.fetchone()
    
        count = row[0];

        conn.close()
        return count
  







