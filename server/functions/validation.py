from database.user_dao import UserDao
from managers.response_helper import ResponseHelper
from utils.string_utils import StringUtils


class Validation(object):

  @classmethod
  def validateToken(self, token):
    if (StringUtils.isEmpty(token)):
      return None, "Invalid token"

    try:
      userDao = UserDao()
      user = userDao.getUser(token)
      if user == None:
        return None, "Invalid token"

      return user, None
    except Exception as ex:
      return None, '''Valid user exception: {}'''.format(str(ex))