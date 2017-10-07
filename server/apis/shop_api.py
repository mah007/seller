from flask_cors import CORS, cross_origin
from flask import Blueprint, request, make_response, jsonify
from controllers.shop.shop_controller import ShopController
from utils.api_utils import ApiUtils
from utils.timestamp_utils import TimestampUtils


ShopAPI = Blueprint('shop_api', __name__, template_folder='apis')

# ------------------------------------------------------------------------------
# Insert
# ------------------------------------------------------------------------------
@ShopAPI.route('/shop/create', methods=['POST'])
@cross_origin()
def createShop():
  if (ApiUtils.checkTokenArgument(request.args) == False):
    return make_response(jsonify({'error': 'Missing token'}), 400)

  if not request.json:
    return make_response(jsonify({'error': 'Missing json parameters value'}), 422)
  if not 'name' in request.json:
    return make_response(jsonify({'error': 'Missing json parameter value'}), 422)
  if not 'email' in request.json:
    return make_response(jsonify({'error': 'Missing json parameter value'}), 422)
  if not 'api_key' in request.json:
    return make_response(jsonify({'error': 'Missing json parameter value'}), 422)

  token = request.args.get('token')
  shop = {
    "name": request.json['name'],
    "email": request.json['email'],
    "api_key": request.json['api_key'],
    "created_at": TimestampUtils.getCurrentDatetime()
  }

  shopCtrl = ShopController()
  result = shopCtrl.createShop(token, shop)
  if 'success' in result:
    return make_response(jsonify(result), 201)
  else:
    return make_response(jsonify(result), 400)









