var endpointUrl = "http://localhost:5000";

var EndpointConfig = function() {

  //----------------------------------------------------------------------------
  // Login section
  //----------------------------------------------------------------------------
  EndpointConfig.prototype.generateUpdateStateSkuEndpoind = function() {
    return endpointUrl + '/sku/update-state?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateLoginEndpoind = function() {
    return endpointUrl + '/user/login';
  }


  //----------------------------------------------------------------------------
  // Sku management section
  //----------------------------------------------------------------------------
  EndpointConfig.prototype.generateGetAllSkuEndpoind = function() {
    return endpointUrl + '/sku/get-all?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateInsertSkuEndpoind = function() {
    return endpointUrl + '/sku/insert?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateUpdateSkuEndpoind = function() {
    return endpointUrl + '/sku/update?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateDeleteSkuEndpoind = function() {
    return endpointUrl + '/sku/delete?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateUpdateStateSkuEndpoind = function() {
    return endpointUrl + '/sku/update-state?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateSearchSku = function() {
    return endpointUrl + '/sku/search?token=' + $.cookie('token');
  }

  //----------------------------------------------------------------------------
  // User management section
  //----------------------------------------------------------------------------
  EndpointConfig.prototype.generateGetAllUserEndpoind = function() {
    return endpointUrl + '/user/get-all?token=' + $.cookie('token') + '&username=' + $.cookie('username');
  }

  EndpointConfig.prototype.generateInsertUserEndpoind = function() {
    return endpointUrl + '/user/insert?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateUpdateUserEndpoind = function() {
    return endpointUrl + '/user/update?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateDeleteUserEndpoind = function() {
    return endpointUrl + '/user/delete?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateUpdateUserPwEndpoind = function() {
    return endpointUrl + '/user/update-password?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateRegisterEndpoind = function() {
    return endpointUrl + '/user/register';
  }

  //----------------------------------------------------------------------------
  // Order management section
  //----------------------------------------------------------------------------
  EndpointConfig.prototype.generateScanOrderEndPoint = function() {
    return endpointUrl + '/order/scan-barcode?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateRefreshAllOrdersEndPoint = function() {
    return endpointUrl + '/order/refresh-all-orders?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateGetAllOrders = function(){
      return endpointUrl + '/order/get-orders?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateUpdateOrderState = function(){
      return endpointUrl + '/order/update-order?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateSetStatusReadyToShipEndPoint = function() {
      return endpointUrl + '/order/ready-to-ship?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateGetFailedOrders = function() {
      return endpointUrl + '/order/get-failed-orders?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateRefreshFailedOrder = function() {
      return endpointUrl + '/order/refresh-failed-orders?token=' + $.cookie('token');
  }


  //----------------------------------------------------------------------------
  // Enemy section
  //----------------------------------------------------------------------------
  EndpointConfig.prototype.generateGetHistory = function() {
      return endpointUrl + '/sku/get-all-history?token=' + $.cookie('token');
  }

  //----------------------------------------------------------------------------
  // Product section
  //----------------------------------------------------------------------------
  EndpointConfig.prototype.generateGetAllProduct = function() {
      return endpointUrl + '/product/get?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateUpdateProduct = function() {
      return endpointUrl + '/product/update?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateUpdateProduct = function() {
      return endpointUrl + '/product/update?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateUpdateProduct = function() {
      return endpointUrl + '/product/update?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateUpdateProductQuantity = function() {
      return endpointUrl + '/product/update-quantity?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateUpdateProductPrice = function() {
      return endpointUrl + '/product/update-price?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateSearchProduct = function() {
      return endpointUrl + '/product/search?token=' + $.cookie('token');
  }

  //----------------------------------------------------------------------------
  // Price by time section
  //----------------------------------------------------------------------------
  EndpointConfig.prototype.generateInsertPriceByTime = function() {
      return endpointUrl + '/price-by-time/insert?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateGetAllPriceByTime = function() {
      return endpointUrl + '/price-by-time/get-all?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateDeletePriceByTime = function() {
      return endpointUrl + '/price-by-time/delete?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateSearchPriceByTime = function() {
      return endpointUrl + '/price-by-time/search?token=' + $.cookie('token');
  }

  //----------------------------------------------------------------------------
  // Product management section
  //----------------------------------------------------------------------------
  EndpointConfig.prototype.generateGetAllProduct = function() {
      return endpointUrl + '/product/get?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateUpdateProduct = function() {
      return endpointUrl + '/product/update?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateUpdateProduct = function() {
      return endpointUrl + '/product/update?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateUpdateProduct = function() {
      return endpointUrl + '/product/update?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateUpdateProductQuantity = function() {
      return endpointUrl + '/product/update-quantity?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateUpdateProductPrice = function() {
      return endpointUrl + '/product/update-price?token=' + $.cookie('token');
  }

  //----------------------------------------------------------------------------
  // Account statemnt section
  //----------------------------------------------------------------------------
  EndpointConfig.prototype.generateGetAccountStatements = function() {
      return endpointUrl + '/account-statement/get-all?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.generateGetAccountStatementInfo = function() {
      return endpointUrl + '/account-statement/get-info?token=' + $.cookie('token');
  }

  EndpointConfig.prototype.getUpdateOriginPriceUrl = function() {
      return endpointUrl + '/account-statement/update-original-prices?token=' + $.cookie('token');
  }

}
















