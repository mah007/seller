import psycopg2
from config import Database


class DatabaseHelper:

	@classmethod
	def execute(self, query):
		try:
			conn = psycopg2.connect(database = Database.DATABASE, user = Database.USER, password = Database.PASSWORD, host = Database.HOST, port = Database.PORT)
			cur = conn.cursor()
			cur.execute(query)
			conn.commit()
			conn.close()
			return True
		except Exception as ex:
			print ex
			return False

	@classmethod
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

	@classmethod
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

	@classmethod
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

	@classmethod
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






