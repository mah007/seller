from config import OrderConfig

class OrderHelper:

  @classmethod
  def getOrderNumberFromBarcode(sefl, barcode):
    if not barcode:
      return None

    if (OrderConfig.BARCODE_START_WITH_1 in barcode) or (OrderConfig.BARCODE_START_WITH_2 in barcode):
      barcode = barcode.replace(OrderConfig.BARCODE_START_WITH_1, "")
      barcode = barcode.replace(OrderConfig.BARCODE_START_WITH_2, "")
      barcode = barcode.replace("-", "")
      return barcode[:-4]  # substract last 4 characters

    return None