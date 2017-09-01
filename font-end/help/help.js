var endpoint = new EndpointConfig();
var cookie = new CookieConfig();

jQuery(document).ready(function() {

    // Validate Token
    if (!cookie.validateLocalToken()) {
        window.location.href = "../login";
    }

    // Fill user name
    $('#username-on-header').html(cookie.getUsername());

    // Load menu left
    $("#menuContent").load("../menuleft.html");
});