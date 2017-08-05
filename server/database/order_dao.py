from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils


class OrderDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS order_management(
        			id 				INT AUTO_INCREMENT primary key NOT NULL,
                    orderID         INTEGER    	NOT NULL,
                    orderNumber     INTEGER     	NOT NULL,
                    userID			INTEGER		NOT NULL,
                    orderJson     	TEXT		NOT NULL,
                    createdAt     	INTEGER    	NOT NULL
                    );'''
        DatabaseHelper.execute(query)


    def getAll(self, user):
        try:
            query = '''SELECT * from order_management WHERE user_id = '{}' ORDER BY id DESC LIMIT 100'''.format(user['id'])
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            orders = []
            rows = cur.fetchall()
            for row in rows:
                orders.append({
                    "id": row[0],
                    "orderID": row[1],
                    "orderNumber": row[2],
                    "userID": row[3],
                    "orderJson": row[4],
                    "createdAt": row[5]
                })

            conn.close()
            return orders
        except Exception as ex:
            print(ex)
            return None

 
    def deleteWithDate(self, createdAt`):
        query = '''DELETE from order_management where createdAt < '{}' '''.format(createdAt)
        DatabaseHelper.execute(query)


    def insert(self, order, user):
        query = '''INSERT INTO order_management (orderID, orderNumber, userID, orderJson, createdAt)
    				VALUES ('{}', '{}', '{}', {}, {})'''.format(
    				order['orderID'], order['orderNumber'], user['userID'],
                    StringUtils.toString(order['orderJson']), order['createdAt'])
        DatabaseHelper.execute(query)

