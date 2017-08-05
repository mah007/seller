from database.sku_dao import SkuDao
from database.user_dao import UserDao
from database.order_dao import OrderDao
from managers.user_manager import UserManager
from lazada_api.lazada_order_api import LazadaOrderApi
from managers.order_helper import OrderHelper
from managers.response_helper import ResponseHelper


class OrderManager(object):

	def initialize(self):
		orderDao = OrderDao()
		orderDao.createTable()


	def validateToken(self, token):
		userDao = UserDao()
		user = userDao.getUser(token)
		if user == None:
			return ResponseHelper.generateErrorResponse("You should log out and login again to use this function !")
		else:
			return user

	def tempOrder(self):
		return {
              "OrderId": 111990523,
                    "CustomerFirstName": "Diem VUONG",
                    "CustomerLastName": "",
                    "OrderNumber": 343327867,
                    "PaymentMethod": "CashOnDelivery",
                    "Remarks": "",
                    "DeliveryInfo": "",
                    "Price": "78,000.00",
                    "GiftOption": False,
                    "GiftMessage": "",
                    "VoucherCode": "",
                    "CreatedAt": "2017-08-04 08:53:11",
                    "UpdatedAt": "2017-08-05 11:16:47",
                    "AddressBilling": {
                        "FirstName": "Diem VUONG",
                        "LastName": "",
                        "Phone": "0908050920",
                        "Phone2": "",
                        "Address1": "164/28 duong so 1",
                        "Address2": "",
                        "Address3": "Hồ Chí Minh",
                        "Address4": "Quận 7",
                        "Address5": "Phường Tân Phú",
                        "CustomerEmail": "",
                        "City": "Hồ Chí Minh-Quận 7-Phường Tân Phú",
                        "PostCode": "",
                        "Country": "Vietnam"
                    },
                    "AddressShipping": {
                        "FirstName": "Diem VUONG",
                        "LastName": "",
                        "Phone": "0908050920",
                        "Phone2": "",
                        "Address1": "164/28 duong so 1",
                        "Address2": "",
                        "Address3": "Hồ Chí Minh",
                        "Address4": "Quận 7",
                        "Address5": "Phường Tân Phú",
                        "CustomerEmail": "",
                        "City": "Hồ Chí Minh-Quận 7-Phường Tân Phú",
                        "PostCode": "",
                        "Country": "Vietnam"
                    },
                    "NationalRegistrationNumber": "",
                    "ItemsCount": 2,
                    "PromisedShippingTimes": "",
                    "ExtraAttributes": "null",
                    "Statuses": [
                        "ready_to_ship"
                    ],
                    "Voucher": 0,
                    "ShippingFee": 0
          }

	#-----------------------------------------------------------------------------
	# Scan barcode
	#-----------------------------------------------------------------------------
	def scanBarcode(self, token, barcode):
		user = self.validateToken(token)
		if 'error' in user:
			return user

		# Get orderNumer
		orderNumber = OrderHelper.getOrderNumberFromBarcode(barcode)
		if not orderNumber:
			return ResponseHelper.generateErrorResponse("Barcode is invalid !")

		# Get order by orderNumber
		orderDao = OrderDao()
		order = orderDao.getOrderByOrderNumber(user, orderNumber)
		order = self.tempOrder()
		if 'error' in order:
			return ResponseHelper.generateErrorResponse(order['error'])

		# Get orderItem by order
		lazadaOrderApi = LazadaOrderApi()
		lazadaOrderItems = lazadaOrderApi.getOrderItems(order, user)
		if 'error' in lazadaOrderItems:
			return ResponseHelper.generateErrorResponse(lazadaOrderItems['error'])

		result = {
			"order": order,
			"orderItems": lazadaOrderItems
		}

		return ResponseHelper.generateSuccessResponse(result)


	#-----------------------------------------------------------------------------
	# Get order by id
	#
	# Refactor later
	#-----------------------------------------------------------------------------
	def getOrder(self, order, user):
		lazadaSkuApi = LazadaOrderApi()
		lazadaOrder = lazadaSkuApi.getOrder(order, user)
		if not lazadaOrder:
			return ResponseHelper.generateErrorResponse("Can't access to Lazada service")

		return ResponseHelper.generateSuccessResponse(lazadaOrder)


	#-----------------------------------------------------------------------------
	# Get orderItem by id
	#
	# Refactor later
	#-----------------------------------------------------------------------------
	def getOrderItems(self, order, user):
		lazadaOrderApi = LazadaOrderApi()
		lazadaOrderItems = lazadaOrderApi.getOrderItems(order, user)
		if not lazadaOrderItems:
			return ResponseHelper.generateErrorResponse("Can't access to Lazada service")

		return ResponseHelper.generateSuccessResponse(lazadaOrderItems)








