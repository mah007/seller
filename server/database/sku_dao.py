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








