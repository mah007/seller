import psycopg2
from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils

class UserDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS t_user(
                    id                  SERIAL		PRIMARY KEY NOT NULL,
                    user_name           TEXT     	NOT NULL,
                    password            TEXT        NOT NULL,
                    token               TEXT        NOT NULL,
                    lazada_user_name    TEXT,
                    lazada_user_id      TEXT,
                    lazada_api_key      TEXT,
                    created_at          INTEGER 	NOT NULL,
                    updated_at          INTEGER
                    );'''
        DatabaseHelper.execute(query)


    def insert(self, user):
        query = '''INSERT INTO t_user (user_name, password, token, lazada_user_name, lazada_user_id, lazada_api_key, created_at, updated_at)
                    VALUES ('{}', '{}', 'temptoken', '{}', '{}', '{}', '{}', 0)'''.format(
                    StringUtils.toString(user['username']),
                    StringUtils.toString(user['password']),
                    StringUtils.toString(user['lazada_user_name']),
                    StringUtils.toString(user['lazada_user_id']),
                    StringUtils.toString(user['lazada_api_key']),
                    user['created_at'])
        DatabaseHelper.execute(query)


    def getUser(self, token):
        try:
            query = '''SELECT id, lazada_user_name, lazada_user_id, lazada_api_key FROM t_user WHERE token='{}' '''.format(StringUtils.toString(token))
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            rows = cur.fetchall()
            if not rows:
                conn.close()
                return None

            user = {
                "id": "",
                "lazada_user_name": "",
                "lazada_user_id": "",
                "lazada_api_key": "",
            }
            for row in rows:
                user['id'] = row[0]
                user['lazada_user_name'] = row[1]
                user['lazada_user_id'] = row[2]
                user['lazada_api_key'] = row[3]

            conn.close()
            return user
        except Exception as ex:
            print(ex)
            return None


    def getAll(self):
        try:
            query = '''SELECT * FROM t_user'''
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            users = []
            rows = cur.fetchall()
            for row in rows:
                users.append({
                        "id": row[0],
                        "username": row[1],
                        "password": row[2],
                        "lazada_user_name": row[4],
                        "lazada_user_id": row[5],
                        "lazada_api_key": row[6]
                })

            conn.close()
            return users
        except Exception as ex:
            print(ex)
            return None


    # --------------------------------------------------------------------------
    # Supported user login
    # <p>
    # Called from:
    # 1. user_manager::login
    # --------------------------------------------------------------------------
    def getUserByUsername(self, username):
        try:
            query = '''SELECT id, lazada_user_name, password FROM t_user WHERE user_name = '{}' '''.format(username)
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            rows = cur.fetchall()
            if not rows:
                cur.close()
                return None

            user = None
            for row in rows:
                user = {
                    "id": row[0],
                    "username": row[1],
                    "password": row[2],
                }

            conn.close()
            return user
        except Exception as ex:
            print(ex)
            return None

    def updateUserToken(self, user):
        try:
            query = '''UPDATE t_user set token = '{}' WHERE id = '{}' '''.format(user['token'], user['id'])
            DatabaseHelper.execute(query)
            return user
        except Exception as ex:
            print(ex)
            return None

    # --------------------------------------------------------------------------
    # Delete User
    # --------------------------------------------------------------------------
    def deleteUser(self, user):
        query = '''DELETE from t_user where id = '{}' '''.format(user['id'])
        DatabaseHelper.execute(query)

    def updateUser(self, user):
        query = '''UPDATE t_user SET password = '{}' WHERE id = '{}' '''.format(user['password'], user['id'])
        DatabaseHelper.execute(query)




