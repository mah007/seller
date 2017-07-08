$("#btnloginsubmit").click(function() {
    console.log("login");
    $.ajax({
        method:'POST',
        url: 'http://localhost:5000/user/login',
        contentType: "application/json",
        data: JSON.stringify({
            username: $('input[name=username]').val(),
            password: $('input[name=password]').val()
        }),
        success: function(data) {
            window.location.href = "/sku-management";
        },
        error: function(error) {
            var exception = JSON.parse(error.responseText);
            swal(exception.error, error, "error");
            console.log(error);
        }
    });
});