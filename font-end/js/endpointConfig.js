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
}