
var CookieConfig = function() {

  CookieConfig.prototype.save = function(name, object) {
    console.log(name, object)
    $.cookie(name, object, {
      path: '/',
      expires: 1
    });
  }

  CookieConfig.prototype.validateLocalToken = function() {
    var token = $.cookie('token');
    return token != null && token.length > 0;
  }
}