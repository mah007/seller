import psycopg2
from database.database_helper import DatabaseHelper
from utils.string_utils import StringUtils
from utils.exception_utils import ExceptionUtils
from config import UserConfig

# ------------------------------------------------------------------------------
# TODO: Handle exception
# ------------------------------------------------------------------------------

class UserDao(object):

    def createTable(self):
        query = '''CREATE TABLE IF NOT EXISTS t_user(
                    id              INT AUTO_INCREMENT primary key NOT NULL,
                    user_name           VARCHAR(200)     	NOT NULL,
                    password            TEXT        NOT NULL,
                    token               TEXT        NOT NULL,
                    lazada_user_name    VARCHAR(200),
                    lazada_user_id      VARCHAR(200),
                    lazada_api_key      TEXT,
                    created_at          INTEGER 	NOT NULL,
                    updated_at          INTEGER,
                    role                INTEGER,
                    certain_size        INTEGER
                    );'''
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Insert User
    # TODO: refactor
    # --------------------------------------------------------------------------
    def insert(self, user):
        query = '''INSERT INTO t_user (user_name, password, token, lazada_user_name, lazada_user_id, lazada_api_key, created_at, updated_at, role, certain_size)
                    VALUES ('{}', '{}', 'temptoken', '{}', '{}', '{}', '{}', 0, '{}', '{}')'''.format(
                    StringUtils.toString(user['username']),
                    StringUtils.toString(user['password']),
                    StringUtils.toString(user['lazada_user_name']),
                    StringUtils.toString(user['lazada_user_id']),
                    StringUtils.toString(user['lazada_api_key']),
                    user['created_at'],
                    user['role'],
                    user['certain_size'])
        DatabaseHelper.execute(query)

    # --------------------------------------------------------------------------
    # Get SuperAdmin
    # Purpose:
    # 1. Get all orders, manage orders.
    # 2. Get all products, manage product.
    # --------------------------------------------------------------------------
    def getSuperAdmin(self):
        query = '''SELECT id, lazada_user_name, lazada_user_id, lazada_api_key
                    FROM t_user
                    WHERE lazada_user_id = '{}' '''.format(UserConfig.SUPER_ADMIN)
        try:
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            row = cur.fetchone()
            if not row:
                conn.close()
                return ExceptionUtils.error('''Dont have any super admins''')

            user = {
                'id': row[0],
                'username': row[1],  # Using lazada user name instead.
                'lazada_user_name': row[1],
                'lazada_user_id': row[2],
                'lazada_api_key': row[3]
            }

            conn.close()
            return user
        except Exception as ex:
            return ExceptionUtils.error('''Get super admin exception: {}'''.format(str(ex)))

    # --------------------------------------------------------------------------
    # Get User
    # TODO: refactor
    # --------------------------------------------------------------------------
    def getUser(self, token):
        try:
            query = '''SELECT id, lazada_user_name, lazada_user_id, lazada_api_key FROM t_user WHERE token='{}' '''.format(StringUtils.toString(token))
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            row = cur.fetchone()
            if not row:
                conn.close()
                return None

            user = {
                'id': row[0],
                'username': row[1],  # Using lazada user name instead.
                'lazada_user_name': row[1],
                'lazada_user_id': row[2],
                'lazada_api_key': row[3]
            }
            conn.close()
            return user
        except Exception as ex:
            print(ex)
            return None

    # --------------------------------------------------------------------------
    # Get User for update password
    # TODO: refactor
    # --------------------------------------------------------------------------
    def getUserUpdatePW(self, token):
        try:
            query = '''SELECT id, user_name, password FROM t_user WHERE token='{}' '''.format(StringUtils.toString(token))
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            row = cur.fetchone()
            if not row:
                conn.close()
                return None

            user = {
                "id": row[0],
                "user_name": row[1],
                "password": row[2],
            }
            conn.close()
            return user
        except Exception as ex:
            print(ex)
            return None

    # --------------------------------------------------------------------------
    # Get all users
    # TODO: refactor
    # --------------------------------------------------------------------------
    def getAll(self):
        try:
            query = '''SELECT * FROM t_user '''
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            users = []
            rows = cur.fetchall()
            for row in rows:
                role = "User"
                if (row[9] == 1):
                    role = "Admin"
                users.append({
                        "id": row[0],
                        "username": row[1],
                        "password": row[2],
                        "lazada_user_name": row[4],
                        "lazada_user_id": row[5],
                        "lazada_api_key": row[6],
                        "role": role,
                        "certain_size": row[10]
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

            row = cur.fetchone()
            if not row:
                cur.close()
                return None

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
        query = '''UPDATE t_user SET password = '{}', lazada_user_id = '{}', lazada_user_name = '{}', lazada_api_key = '{}', certain_size = '{}' WHERE id = '{}' '''.format(
                    user['password'], user['lazada_userid'], user['lazada_username'], user['lazada_apikey'], user['certain_size'], user['id'])
        DatabaseHelper.execute(query)


    def updatePw(self, user, token):
        try:
            query = '''UPDATE t_user SET password = '{}' WHERE token = '{}' '''.format(user['newpass'], token)
            DatabaseHelper.execute(query)
            return user;
        except Exception as ex:
            print(ex)
            return None

    # --------------------------------------------------------------------------
    # TODO: change this function to isAdminUser
    # Return Boolean
    # --------------------------------------------------------------------------
    def getAdminUser(self, userid):
        try:
            query = '''SELECT * FROM t_user WHERE id = '{}' AND role = 1 '''.format(userid)
            conn = DatabaseHelper.getConnection()
            cur = conn.cursor()
            cur.execute(query)

            row = cur.fetchone()
            if not row:
                cur.close()
                return None

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


    def getCertainSize(self, id):
        query = ''' SELECT certain_size FROM t_user WHERE id = '{}' '''.format(id)
        conn = DatabaseHelper.getConnection()
        cur = conn.cursor()
        cur.execute(query)

        count = 0
        row = cur.fetchone()
        count = row[0];

        conn.close()
        return count




