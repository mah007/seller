
class ResponseHelper:

  @classmethod
  def generateErrorResponse(self, errorMessage):
    return {"error": errorMessage}


  @classmethod
  def generateSuccessResponse(self, result):
    return {"success": "done", "data": result}


  @classmethod
  def generateSuccessResponse(self, message, result):
    return {"success": message, "data": result}


  @classmethod
  def convertToArryError(self, errorMessage):
    errorArray = []
    errorArray.append(errorMessage)
    return errorArray