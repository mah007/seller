from utils.string_utils import StringUtils


class ApiUtils(object):

    @classmethod
    def checkTokenArgument(self, argument):
      if (not argument):
        return False
      if not 'token' in argument:
        return False
      token = argument.get('token')
      return not StringUtils.isEmpty(token)

















