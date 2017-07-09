$("#btnloginsubmit").click(function() {
    $.ajax({
        method:'POST',
        url: 'http://localhost:5000/user/login',
        contentType: "application/json",
        data: JSON.stringify({
            username: $('input[name=username]').val(),
            password: $.md5($('input[name=password]').val(), "leoz")
        }),
        success: function(data) {
            // console.log(data.data, data.data.token);
            var userObj = data.data;
            $.cookie('userJson', data.data, { expires: 1 });
            $.cookie('token', userObj.token, { expires: 1 });
            window.location.href = "/sku-management";
        },
        error: function(error) {
            var exception = JSON.parse(error.responseText);
            swal("Failed", exception.error, "error");
        }
    });
});