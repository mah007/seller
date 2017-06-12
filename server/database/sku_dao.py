import psycopg2
from database.database_helper import DatabaseHelper


class SkuDao(Object):

    def createTable(self):
        query = '''CREATE TABLE COMPANY(ID INT PRIMARY KEY NOT NULL,
                    NAME           TEXT    NOT NULL,
                    AGE            INT     NOT NULL,
                    ADDRESS        CHAR(50),
                    SALARY         REAL);'''

        DatabaseHelper.execute(query)










