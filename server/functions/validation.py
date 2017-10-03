from database.user_dao import UserDao
from managers.response_helper import ResponseHelper

# Instances
userDao = UserDao()


class Validation(object):

  @classmethod
  def validateToken(self, token):
    try:
      user = userDao.getUser(token)
      if user == None:
        return None, "Invalid token"

      return user, None
    except Exception as ex:
      return None, '''Valid user exception: {}'''.format(str(ex))