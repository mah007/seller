var endpoint = "http://localhost:5000";

var LeoZ = function() {

  LeoZ.prototype.generateGetAllSkuEndpoind = function() {
    console.log("LeoZ", $.cookie('token'));
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
}