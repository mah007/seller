from database.database_helper import DatabaseHelper


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






