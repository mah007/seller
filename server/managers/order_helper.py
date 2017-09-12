import time
import json
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

  @classmethod
  def convertLazadaOrderToOrder(self, lazadaOrder):
    order = {
      "order_id": lazadaOrder['OrderId'],
      "order_number": lazadaOrder['OrderNumber'],
      "price": lazadaOrder['Price'],
      "customer_name": lazadaOrder['CustomerFirstName'],
      "customer_phone": "",
      "customer_email": "",
      "address_shipping": "",
      "voucher_code": lazadaOrder['VoucherCode'],
      "voucher_price": lazadaOrder['Voucher'],
      "delivery_info": lazadaOrder['DeliveryInfo'],
      "payment_method": lazadaOrder['PaymentMethod'],
      "remarks": lazadaOrder['Remarks'],
      "gift_message": lazadaOrder['GiftMessage'],
      "shipping_fee": lazadaOrder['ShippingFee'],
      "status": "",
      "created_at": lazadaOrder['CreatedAt'],
      "updated_at": lazadaOrder['UpdatedAt'],
      "order_json": json.dumps(lazadaOrder, ensure_ascii=False)
    }

  @classmethod
  def convertOrderToLazadaOrder(self, order):
    return json.loads(order['order_json'])








