import pymysql
from config import Database


class DatabaseHelper:

	@classmethod
	def getConnection(self):
		return pymysql.connect(**Database.mysql)

	@classmethod
	def execute(self, query):
		conn = pymysql.connect(**Database.mysql)
		cur = conn.cursor()

		try:
			cur.execute(query)
			conn.commit()
		except Exception as ex:
			conn.rollback()
			print(query)
			return False, str(ex)

		conn.close()
		return True, None






