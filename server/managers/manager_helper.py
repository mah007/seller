from database.user_dao import UserDao
from managers.response_helper import ResponseHelper


class ManagerHelper(object):

  @classmethod
  def validateToken(self, token):
    userDao = UserDao()
    try:
      user = userDao.getUser(token)
      if user == None:
        return ResponseHelper.generateErrorResponse("Invalid token")

      return user
    except Exception as ex:
      return ResponseHelper.generateErrorResponse('''Validate user exception: {}'''.format(str(ex)))