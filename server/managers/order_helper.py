from config import OrderConfig

class OrderHelper:

  @classmethod
  def getOrderNumberFromBarcode(sefl, barcode):
    if not barcode:
      return None

    if (OrderConfig.BARCODE_START_WITH_1 not in barcode) or (OrderConfig.BARCODE_START_WITH_2 not in barcode):
      return None

    barcode = barcode.replace(OrderConfig.BARCODE_START_WITH_1, "")
    barcode = barcode.replace(OrderConfig.BARCODE_START_WITH_2, "")
    barcode = barcode.replace("-", "")
    return barcode[:-4]  # substract last 4 characters