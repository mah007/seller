
# ------------------------------------------------------------------------------
# Deprecated now
# Please using response_utils.py instead.

class ResponseHelper:

  @classmethod
  def generateErrorResponse(self, errorMessage):
    return {"error": errorMessage}


  @classmethod
  def generateSuccessResponse(self, result):
    return {"success": "done", "data": result}
