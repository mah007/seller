

class ResponseUtils:

  @classmethod
  def returnError(self, errorMessage):
    return {"error": errorMessage}

  @classmethod
  def returnSuccess(self, data, message="success"):
    return {"success": message, "data": data}

  # NOTE:
  # This function has been deprecated
  @classmethod
  def generateSuccessResponse(self, message="done", result=None):
    return {"success": message, "data": result}

  # NOTE:
  # This function has been deprecated
  @classmethod
  def generateSuccessResponse(self, result=None):
    return {"success": "done", "data": result}

  @classmethod
  def convertToArryError(self, errorMessage):
    errorArray = []
    errorArray.append(errorMessage)
    return errorArray



