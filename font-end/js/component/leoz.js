var endpoint = "http://localhost:5000";

var LeoZ = function() {

  //----------------------------------------------------------------------------
  // Login section
  //----------------------------------------------------------------------------
  LeoZ.prototype.generateUpdateStateSkuEndpoind = function() {
    return endpoint + '/sku/update-state?token=' + $.cookie('token');
  }

  LeoZ.prototype.generateLoginEndpoind = function() {
    return endpoint + '/user/login';
  }


  //----------------------------------------------------------------------------
  // Sku management section
  //----------------------------------------------------------------------------
  LeoZ.prototype.generateGetAllSkuEndpoind = function() {
    return endpoint + '/sku/get-all?token=' + $.cookie('token');
  }

  LeoZ.prototype.generateInsertSkuEndpoind = function() {
    return endpoint + '/sku/insert?token=' + $.cookie('token');
  }

  LeoZ.prototype.generateUpdateSkuEndpoind = function() {
    return endpoint + '/sku/update?token=' + $.cookie('token');
  }

  LeoZ.prototype.generateDeleteSkuEndpoind = function() {
    return endpoint + '/sku/delete?token=' + $.cookie('token');
  }

  LeoZ.prototype.generateUpdateStateSkuEndpoind = function() {
    return endpoint + '/sku/update-state?token=' + $.cookie('token');
  }

  LeoZ.prototype.validateLocalToken = function() {
    var token = $.cookie('token');
    return token != null && token.length > 0;
  }
}