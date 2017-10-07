
class ExceptionUtils:

  # NOTE: deprecated
  @classmethod
  def error(self, errorMessage):
    return {"error": errorMessage}
  # NOTE: deprecated
  @classmethod
  def success(self, message = None):
    return {"sucess": message}

  # TODO: Will move to another class
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
      return "Response is null"
    if ('ErrorResponse' not in errorResponse):
      return "Dont have ErrorResponse"

    error = errorResponse['ErrorResponse']

    # Get error message from Head
    errorMessageStr = "Empty error message string"
    if ('Head' in error and 'ErrorMessage' in error['Head']):
      errorMessageStr = error['Head']['ErrorMessage']

    # Get error message from Body
    if 'Body' not in error:
      return errorMessageStr
    errorBody = error['Body']
    if 'Errors' not in errorBody:
      return errorMessageStr
    if len(errorBody['Errors']) == 0:
      return "No error message found"
    errorMessage = errorBody['Errors'][0]
    if 'Message' not in errorMessage:
      return "No error message found"

    return errorMessage['Message']











