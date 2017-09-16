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
      "name": str(lazadaProduct['Attributes']['name'],).replace("'", ""),
      "url": lazadaProduct['Skus'][0]['Url'],
      "status": lazadaProduct['Skus'][0]['Status'],
      "quantity": 0,
      "seller_sku": lazadaProduct['Skus'][0]['SellerSku'],
      "shop_sku": lazadaProduct['Skus'][0]['ShopSku'],
      "original_price": 0,
      "image": lazadaProduct['Skus'][0]['Images'][0],
      "package_width": lazadaProduct['Skus'][0]['package_width'],
      "package_height": lazadaProduct['Skus'][0]['package_height'],
      "package_weight": lazadaProduct['Skus'][0]['package_weight'],
      "brand": str(lazadaProduct['Attributes']['brand']).replace("'", ""),
      "model": lazadaProduct['Attributes']['model'],
      "primary_category": lazadaProduct['PrimaryCategory'],
      "spu_id": 0
    }

    # Some products doesn't have this field
    if 'spu_id' in lazadaProduct:
      product['spu_id'] = lazadaProduct['SPUId']

    return product











