from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.lazada_api_helper import LazadaApiHelper

from database.database_helper import DatabaseHelper
from config import ShopConfig


class ShopDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS `shop` (
                    id                  INT AUTO_INCREMENT primary key NOT NULL,
                    name                VARCHAR(100)    NOT NULL,
                    email               VARCHAR(200)    NOT NULL,
                    api_key             VARCHAR(300)    NOT NULL,
                    status              VARCHAR(50)     NOT NULL,
                    user_id             INTEGER         NOT NULL,
                    created_at          DATETIME
                );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert
    # --------------------------------------------------------------------------
    def insert(self, user, shop):
        query = '''INSERT INTO `shop`(name, email, api_key, status, user_id, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)'''
        conn = DatabaseHelper.getConnection()
        cur = conn.cursor()
        try:
            cur.execute(query, (shop['name'], shop['email'], shop['api_key'],
                                ShopConfig.STATE_PROCESSING, user['id'], shop['created_at']))
            conn.commit()
            conn.close()
            return None, None
        except Exception as ex:
            conn.rollback()
            conn.close()
            return None, '''User: {}-{}, Insert-Shop: {}'''.format(user['username'], user['id'], str(ex))













