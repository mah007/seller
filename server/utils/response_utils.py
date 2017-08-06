
# Deprecated now

class ResponseUtils:

  @classmethod
  def generateErrorResponse(self, errorMessage):
    return {"error": errorMessage}


  @classmethod
  def generateSuccessResponse(self, message, result):
    return {"success": message, "data": result}


  @classmethod
  def convertToArryError(self, errorMessage):
    errorArray = []
    errorArray.append(errorMessage)
    return errorArray