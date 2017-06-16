from database.database_helper import DatabaseHelper


class SkuDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS sku_management(
        			id 				SERIAL		PRIMARY KEY NOT NULL,
                    sku           	TEXT    	NOT NULL,
                    name          	TEXT     	NOT NULL,
                    link			TEXT		NOT NULL,
                    min_price     	INTEGER		NOT NULL,
                    max_price     	INTEGER    	NOT NULL,
                    subtract_price 	INTEGER 	NOT NULL,
                    state			INTEGER		NOT NULL,
                    repeat_time 	INTEGER 	NOT NULL,
                    created_at 		INTEGER 	NOT NULL,
                    updated_at		INTEGER 	
                    );'''
        DatabaseHelper.execute(query)


    def getAll(self):
        try:
            query = '''SELECT * from sku_management ORDER BY id DESC LIMIT 100'''
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
                    "subtract_price": row[6],
                    "state": row[7],
                    "repeat_time": row[8],
                    "created_at": row[9],
                })

            conn.close()
            return skus
        except Exception as ex:
            print ex
            return None

    
    def insert(self, sku):
    	query = '''INSERT INTO sku_management (sku, name, link, min_price, max_price, 
    				subtract_price, state, repeat_time, created_at, updated_at) 
    				VALUES ('{}', '{}', '{}', {}, {}, {}, {}, {}, {}, 0)'''.format(
    				sku['sku'], sku['name'], sku['link'], sku['min_price'], sku['max_price'], 
    				sku['subtract_price'], sku['state'], sku['repeat_time'], sku['created_at'])
    	DatabaseHelper.execute(query)


    def update(self, sku):
    	query = '''UPDATE sku_management set sku = '{}', name = '{}', link = '{}', min_price = {}, max_price = {}, 
    				subtract_price = {}, state = {}, repeat_time = {}, updated_at = {})'''.format(
    				sku['sku'], sku['name'], sku['link'], sku['min_price'], sku['max_price'], 
    				sku['subtract_price'], sku['state'], sku['repeat_time'], sku['updated_at'])
    	DatabaseHelper.execute(query)








