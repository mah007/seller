import psycopg2
from constants import Database


class DatabaseHelper(object):
	
	def insert(self, query):
		try:
			conn = psycopg2.connect(database = Database.DATABASE, user = Database.USER, password = Database.PASSWORD, host = Database.HOST, port = Database.PORT)
			cur = conn.cursor()
			cur.execute(query)
			conn.commit()
			conn.close()
			return True
		except Exception as ex:
			return False

	def select(self, query):
		try:
			conn = psycopg2.connect(database = Database.DATABASE, user = Database.USER, password = Database.PASSWORD, host = Database.HOST, port = Database.PORT)
			cur = conn.cursor()
			cur.execute(query)
			rows = cur.fetchall()
			for row in rows:
			   print "ID = ", row[0]
			conn.close()
			return None
		except Exception as ex:
			return None

	def update(self, query):
		try:
			conn = psycopg2.connect(database = Database.DATABASE, user = Database.USER, password = Database.PASSWORD, host = Database.HOST, port = Database.PORT)
			cur = conn.cursor()
			cur.execute(query)
			conn.commit()
			conn.close()
			return True
		except Exception as ex:
			return False

	def delete(self, query):
		try:
			conn = psycopg2.connect(database = Database.DATABASE, user = Database.USER, password = Database.PASSWORD, host = Database.HOST, port = Database.PORT)
			cur = conn.cursor()
			cur.execute(query)
			conn.commit()
			conn.close()
			return True
		except Exception as ex:
			return False






