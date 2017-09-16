import time
import json
from config import OrderConfig

class ConvertHelper:

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

  @classmethod
  def convertLazadaProductToProduct(self, lazadaProduct):
    product = {
      "name": lazadaProduct['Attributes']['name'],
      "url": lazadaProduct['Skus'][0]['Url'],
      "status": lazadaProduct['Skus'][0]['Status'],
      "quantity": 0,
      "seller_sku": lazadaProduct['Skus'][0]['SellerSku'],
      "shop_sku": lazadaProduct['Skus'][0]['ShopSku'],
      "original_price": 0,
      "image": json.dumps(lazadaProduct['Skus'][0]['Images'], ensure_ascii=False),
      "package_width": lazadaProduct['Skus'][0]['package_width'],
      "package_height": lazadaProduct['Skus'][0]['package_height'],
      "package_weight": lazadaProduct['Skus'][0]['package_weight'],
      "brand": lazadaProduct['Attributes']['brand'],
      "model": lazadaProduct['Attributes']['model'],
      "primary_category": lazadaProduct['PrimaryCategory'],
      "created_time": "",
      "sku_id": "",
      "user_id": ""
    }

    return product

    









