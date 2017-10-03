from database.database_helper import DatabaseHelper


# NOTE: add priority for exception

# Error: UI => light red color, add message to user should check order/product, if there is any issue please contact developer
# 1. Not found Order
# 2. Not found OrderItem.
# 3. Not found Product.

# Warning: UI => light yellow color
# 4. OrderItem >> item_price not equal with OrderItem >> paid_price
# 5. OrderItem >> paid_price not equal wiht Lazada >> sales_deliver
# 6. Order status not equal delivered

# Issue: UI => contact developer
# 7. Set OrderItem income
# 8. Mark order as calculated

class AccountStatementExceptionDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS `account_statement_exception` (
                id                      BIGINT AUTO_INCREMENT primary key NOT NULL,
                order_number            BIGINT,
                reason                  VARCHAR(300),
                created_at              DATETIME,
                account_statement_id    BIGINT NOT NULL,
                user_id                 BIGINT NOT NULL
                );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert an exception
    # --------------------------------------------------------------------------
    def insert(self, user, orderNumber, accountStatementId, reason, createdAt):
        query = '''INSERT INTO `account_statement_exception`(order_number, reason,
                            created_at, account_statement_id, user_id)
                    VALUES (%s, %s, %s, %s, %s)'''
        conn = DatabaseHelper.getConnection()
        cur = conn.cursor()
        try:
            cur.execute(query, (orderNumber, reason, createdAt, accountStatementId, user['id']))
            conn.commit()
            conn.close()
            return None
        except Exception as ex:
            conn.rollback()
            conn.close()
            return '''User: {}-{}, Insert-Account-Statement-Exception: {}'''.format(user['username'], user['id'], str(ex))


    # --------------------------------------------------------------------------
    # Get an Account Exception
    # --------------------------------------------------------------------------
    def getAll(self, user, accountStatementId):
        query = ''' SELECT *
                    FROM account_statement_exception
                    WHERE user_id = {} AND account_statement_id = {}
                    LIMIT 5
                '''.format(user['id'], accountStatementId)
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            result = []
            rows = cur.fetchall()
            for row in rows:
                result.append({
                    "id": row[0],
                    "order_number": row[1],
                    "reason": row[2],
                    "created_at": row[3]
                })

            conn.close()
            return result, None
        except Exception as ex:
            return None, '''User: {}-{}, Get-Account-Statement-Exception: {}'''.format(user['username'], user['id'], str(ex))



