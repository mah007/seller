
class ExceptionUtils:

  @classmethod
  def error(self, errorMessage):
    return {"error": errorMessage}

  @classmethod
  def success(self, message = None):
    return {"sucess": message}