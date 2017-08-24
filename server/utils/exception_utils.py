
class ExceptionUtils:

  @classmethod
  def error(self, errorMessage):
    return {"error": errorMessage}

  @classmethod
  def success(self, message = None):
    return {"sucess": message}

  @classmethod
  def returnError(self, message, errorResponse):
    if errorResponse == None:
      message += "Unknown error"
      return {"error": message}

    if 'ErrorResponse' not in errorResponse:
      message += str(errorResponse)
      return {"error": message}

    error = errorResponse['ErrorResponse']
    if 'Head' not in error:
      message += str(errorResponse)
      return {"error": message}

    head = error['Head']
    if 'ErrorMessage' not in head:
      message += str(errorResponse)
      return {"error": message}

    message += head['ErrorMessage']
    return {"error": message}
