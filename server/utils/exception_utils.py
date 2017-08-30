
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

    bodyMessage = self.getBodyMessage(errorResponse)
    if bodyMessage != None:
      message += bodyMessage
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

  @classmethod
  def getBodyMessage(self, errorResponse):
    if errorResponse == None:
      return None
    if 'ErrorResponse' not in errorResponse:
      return None

    error = errorResponse['ErrorResponse']
    if 'Body' not in error:
      return None
    errorBody = error['Body']
    if 'Errors' not in errorBody:
      return None
    if len(errorBody['Errors']) == 0:
      return None
    errorMessage = errorBody['Errors'][0]
    if 'Message' not in errorMessage:
      return None

    return errorMessage['Message']











