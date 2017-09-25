import time
import json
from config import OrderConfig

class ConvertHelper:

  # --------------------------------------------------------------------------
  # Get OrderNumber from barcode
  # --------------------------------------------------------------------------
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

  # --------------------------------------------------------------------------
  # Parse LazadaOrderJson to LazadaOrder
  # --------------------------------------------------------------------------
  @classmethod
  def convertOrderToLazadaOrder(self, order):
    return json.loads(order['order_json'])

  # --------------------------------------------------------------------------
  # Convert string to boolean
  # --------------------------------------------------------------------------
  @classmethod
  def str2bool(self, value):
    return {"True": True, "true": True}.get(value, False)

  # --------------------------------------------------------------------------
  # Convert lazadaOrder to Order
  # --------------------------------------------------------------------------
  @classmethod
  def convertLazadaOrderToOrder(self, lazadaOrder):
    return {
      "order_id": lazadaOrder['OrderId'],
      "customer_first_name": lazadaOrder['CustomerFirstName'].replace("'", ""),
      "customer_lastName": lazadaOrder['CustomerLastName'].replace("'", ""),
      "order_number": lazadaOrder['OrderNumber'],
      "payment_method": lazadaOrder['PaymentMethod'],
      "remarks": lazadaOrder['Remarks'],
      "delivery_info": lazadaOrder['DeliveryInfo'],
      "price": float(lazadaOrder['Price'].replace(",", "")),
      "gift_option": int(bool(self.str2bool(lazadaOrder['GiftOption']))),
      "gift_message": lazadaOrder['GiftMessage'],
      "voucher_code": lazadaOrder['VoucherCode'],
      "created_at": lazadaOrder['CreatedAt'],
      "updated_at": lazadaOrder['UpdatedAt'],
      "address_billing": json.dumps(lazadaOrder['AddressBilling'], ensure_ascii=False).replace("'", "").replace("\\", ""),
      "address_shipping": json.dumps(lazadaOrder['AddressShipping'], ensure_ascii=False).replace("'", "").replace("\\", ""),
      "national_registration_number": lazadaOrder['NationalRegistrationNumber'],
      "items_count": lazadaOrder['ItemsCount'],
      "promised_shipping_times": lazadaOrder['PromisedShippingTimes'],
      "extra_attributes": lazadaOrder['ExtraAttributes'],
      "statuses": json.dumps(lazadaOrder['Statuses'], ensure_ascii=False),
      "voucher": lazadaOrder['Voucher'],
      "shipping_fee": lazadaOrder['ShippingFee'],
    }

  # --------------------------------------------------------------------------
  # Convert lazadaOrderItem to OrderItem
  # --------------------------------------------------------------------------
  @classmethod
  def convertLazadaOrderItemToOrderItem(self, lazadaOrderItem):
    return {
      "order_item_id": lazadaOrderItem["OrderItemId"],
      "shop_id": lazadaOrderItem["ShopId"],
      "order_id": lazadaOrderItem["OrderId"],
      "name": lazadaOrderItem["Name"],
      "seller_sku": lazadaOrderItem["Sku"],
      "shop_sku": lazadaOrderItem["ShopSku"],
      "shipping_type": lazadaOrderItem["ShippingType"],
      "item_price": lazadaOrderItem["ItemPrice"],
      "paid_price": lazadaOrderItem["PaidPrice"],
      "currency": lazadaOrderItem["Currency"],
      "wallet_credit": lazadaOrderItem["WalletCredits"],
      "tax_amount": lazadaOrderItem["TaxAmount"],
      "shipping_amount": lazadaOrderItem["ShippingAmount"],
      "shipping_service_cost": lazadaOrderItem["ShippingServiceCost"],
      "voucher_amount": lazadaOrderItem["VoucherAmount"],
      "voucher_code": lazadaOrderItem["VoucherCode"],
      "status": lazadaOrderItem["Status"],
      "shipment_provider": lazadaOrderItem["ShipmentProvider"],
      "is_digital": lazadaOrderItem["IsDigital"],
      "digital_delivery_info": lazadaOrderItem["DigitalDeliveryInfo"],
      "tracking_code": lazadaOrderItem["TrackingCode"],
      "tracking_code_pre": lazadaOrderItem["TrackingCodePre"],
      "reason": lazadaOrderItem["Reason"],
      "reason_detail": lazadaOrderItem["ReasonDetail"],
      "purchase_order_id": lazadaOrderItem["PurchaseOrderId"],
      "purchase_order_number": lazadaOrderItem["PurchaseOrderNumber"],
      "package_id": lazadaOrderItem["PackageId"],
      "promised_shipping_time": lazadaOrderItem["PromisedShippingTime"],
      "extra_attributes": lazadaOrderItem["ExtraAttributes"],
      "shipping_provider_type": lazadaOrderItem["ShippingProviderType"],
      "created_at": lazadaOrderItem["CreatedAt"],
      "updated_at": lazadaOrderItem["UpdatedAt"],
      "return_status": lazadaOrderItem["ReturnStatus"],
      "product_main_image": lazadaOrderItem["productMainImage"],
      "variation": lazadaOrderItem["Variation"],
      "product_detail_url": lazadaOrderItem["ProductDetailUrl"],
      "invoice_number": lazadaOrderItem["invoiceNumber"]
    }

  # --------------------------------------------------------------------------
  # Convert LazadaProduct to Product
  # --------------------------------------------------------------------------
  @classmethod
  def convertLazadaProductToProduct(self, lazadaProduct):
    product = {
      "name": lazadaProduct['Attributes']['name'],
      "status": lazadaProduct['Skus'][0]['Status'],
      "quantity": 0,
      "seller_sku": lazadaProduct['Skus'][0]['SellerSku'],
      "original_price": 0,
      "special_price": lazadaProduct['Skus'][0]['special_price'],
      "image": lazadaProduct['Skus'][0]['Images'][0],
      "package_width": lazadaProduct['Skus'][0]['package_width'],
      "package_height": lazadaProduct['Skus'][0]['package_height'],
      "package_weight": lazadaProduct['Skus'][0]['package_weight'],
      "brand": lazadaProduct['Attributes']['brand'],
      "model": lazadaProduct['Attributes']['model'],
      "primary_category": lazadaProduct['PrimaryCategory'],
      "spu_id": 0,      # Default value
      "url": "",        # Default value
      "shop_sku": ""   # Default value
    }

    # Some products doesn't have this field
    if 'spu_id' in lazadaProduct:
      product['spu_id'] = lazadaProduct['SPUId']
    if 'Url' in lazadaProduct['Skus'][0]:
      product['url'] = lazadaProduct['Skus'][0]['Url']
    if 'ShopSku' in lazadaProduct['Skus'][0]:
      product['shop_sku'] = lazadaProduct['Skus'][0]['ShopSku']

    return product









