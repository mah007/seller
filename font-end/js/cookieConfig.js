
var CookieConfig = function() {

  CookieConfig.prototype.save = function(name, object) {
    $.cookie(name, object, {
      path: '/',
      expires: 1
    });
  }

  CookieConfig.prototype.validateLocalToken = function() {
    var token = $.cookie('token');
    return token != null && token.length > 0;
  }

  CookieConfig.prototype.clearToken = function(name) {
    $.removeCookie(name, {path: '/'});
  }

  CookieConfig.prototype.getToken = function() {
    var token = $.cookie('token');
    return token;
  }

  CookieConfig.prototype.getUsername = function() {
    return $.cookie('username');
  }
}