var endpoint = new EndpointConfig();
var cookie = new CookieConfig();

function validNull(selector) {
    if ($(selector).length > 0) {
        if ($(selector).prop("tagName").toLowerCase() == "select") {
            return ($(selector).val() > 0) ? true : false;
        } else {
            return ($(selector).val().length > 0) ? true : false;
        }
    } else {
        return false;
    }
}

function registerUser() {

    var txt_username = $('input[name=txt_username]').val();
    var txt_password = $('input[name=txt_password]').val();
    var txt_repassword = $('input[name=txt_repassword]').val();
    var txt_lazada_email = $('input[name=txt_lazada_email]').val();
    var txt_lazada_apikey = $('input[name=txt_lazada_apikey]').val();

    var $this = $(this);
    var error = "";

    if (validNull('input[name=txt_username]')) {
        $('input[name=txt_username]').removeClass('has-error');
    } else {
        error += "Username không được bỏ trống.\n";
        $('input[name=txt_username]').addClass('has-error');
    }
    if (validNull('input[name=txt_password]')) {
        $('input[name=txt_password]').removeClass('has-error');
    } else {
        error += "Password không được bỏ trống.\n";
        $('input[name=txt_password]').addClass('has-error');
    }
    if (validNull('input[name=txt_repassword]')) {
        $('input[name=txt_repassword]').removeClass('has-error');
    } else {
        error += "Repeat Password không được bỏ trống.\n";
        $('input[name=txt_repassword]').addClass('has-error');
    }
    if (validNull('input[name=txt_lazada_email]')) {
        $('input[name=txt_lazada_email]').removeClass('has-error');
    } else {
        error += "Lazad Email không được bỏ trống.\n";
        $('input[name=txt_lazada_email]').addClass('has-error');
    }
    if (validNull('input[name=txt_lazada_api_key]')) {
        $('input[name=txt_lazada_api_key]').removeClass('has-error');
    } else {
        error += "Lazada API Key không được bỏ trống.\n";
        $('input[name=txt_lazada_api_key]').addClass('has-error');
    }
    if ($('input[name=txt_password]').hasClass('has-error') == false && $('input[name=txt_repassword]').hasClass('has-error') == false) {
        var pass = ($('input[name=txt_password]').val());
        var repass = ($('input[name=txt_repassword]').val());
        if (repass == pass) {
            $('input[name=txt_password]').removeClass('has-error');
            $('input[name=txt_repassword]').removeClass('has-error');
        } else {
            error += "Repeat passwork và passwork phải giống nhau.\n";
            $('input[name=txt_password]').addClass('has-error');
            $('input[name=txt_repassword]').addClass('has-error');
        }
    }

    if (error.length > 0) {
        swal("Không hợp lệ", error, "error");
        return;
    } else {
        $.ajax({
            method: 'POST',
            url: endpoint.generateRegisterEndpoind(),
            contentType: "application/json",
            data: JSON.stringify({
                username: $('input[name=txt_username]').val(),
                password: $('input[name=txt_password]').val(),
                lazada_email: $('input[name=txt_lazada_email]').val(),
                lazada_api_key: $('input[name=txt_lazada_api_key]').val()
            }),
            success: function(data) {
                var user = JSON.parse(data);
                cookie.save('myUser', user.data);
                cookie.save('token', user.data.token);
                window.location.href = "../sku-management/";
            },
            error: function(error) {
                alert("Username already used!");
                console.log(error);
                var exception = JSON.parse(error.responseText);
                var errorTag = $this.parent().find('.error');
                errorTag.html(exception.error).removeClass('hidden')
            }
        })
    }


}