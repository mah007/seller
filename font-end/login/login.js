var endpoint = new EndpointConfig();
var cookie = new CookieConfig();

jQuery(document).ready(function() {
    if (cookie.validateLocalToken()) {
        window.location.href = "../sku-management";
    }
});

$("#btnloginsubmit").click(function() {
    $.ajax({
        method:'POST',
        url: endpoint.generateLoginEndpoind(),
        contentType: "application/json",
        data: JSON.stringify({
            username: $('input[name=username]').val(),
            password: $('input[name=password]').val()
        }),
        success: function(data) {
            var userObj = data.data;
            console.log(userObj);
            cookie.save('myUser', data.data);
            cookie.save('token', userObj.token);
            window.location.href = "../sku-management"; 
        },
        error: function(error) {
            var exception = JSON.parse(error.responseText);
            swal("Failed", exception.error, "error");
        }
    });
});