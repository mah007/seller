// var leoz = new LeoZ();
var cookie = new CookieConfig();

jQuery(document).ready(function() {

    // Init data
    getAndFillOutAllUser();

    if($('.btnnew').length > 0) {
        $(".btnnew").click(function() {
            $('#portlet-user').attr('data-type', "insert");            
            $('#portlet-user').modal('show');
            $('input[name=txt_id').prop('disabled', true);
        });
    }

});
function enableSwitchery() {

    // Delete User---------------------------------------------------------------
    if($('.btndel').length > 0) {
        $('.btndel').click(function() {
            var id = $(this).parents('tr').data('id');
            swal({
                title: "Are you sure?",
                text: "You will not be able to recover this USER!",
                type: "warning",
                showReloadButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Yes, delete it!",
                closeOnConfirm: false
            }, function () {
                $.ajax({
                    method:'POST',
                    // url: leoz.generateDeleteSkuEndpoind(),
                    url: 'http://localhost:5000/user/delete',
                    contentType: "application/json",
                    data: JSON.stringify({
                        id: id
                    }),
                    success: function(data) {
                        swal({
                            title: "Deleted!",
                            text: "",
                            type: "success",
                            confirmButtonText: "OK! Redirect to list",
                        }, function () {
                            window.location.href = "http://localhost:8000/lazada-seller/font-end/user-management/";
                        });
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            });
        });
    }

    // Edit User---------------------------------------------------------------
    if($('.btnedt').length > 0) {
        $(".btnedt").click(function() {
            var parent = $(this).parents('tr');
            var id = parent.data('id');
            var username = parent.data('user_name');
            var password = parent.data('password');
            var lazada_username = parent.data('lazada_user_name');
            var lazada_userid = parent.data('lazada_user_id');
            var lazada_apikey = parent.data('lazada_api_key');

            $('#portlet-user').attr('data-type', "edit");
            $('#portlet-user .modal-title').html('Chỉnh sửa ' + username);
            $('input[name=txt_id').val(id).prop('disabled', true);

            $('input[name=txt_username]').val(username).prop('disabled', true);
            $('input[name=txt_lazada_username]').val(lazada_username).prop('disabled', true);
            $('input[name=txt_lazada_userid]').val(lazada_userid).prop('disabled', true);
            $('input[name=txt_lazada_apikey]').val(lazada_apikey).prop('disabled', true);

            $('#portlet-user').modal('show');
        });
    }

}

function validNull (selector) {
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

$(".btnmodalsubmit").click(function() {
    var txt_username = $('input[name=txt_username]').val();
    var txt_password = $('input[name=txt_password]').val();
    var txt_lazada_username = $('input[name=txt_lazada_username]').val();
    var txt_lazada_userid = $('input[name=txt_lazada_userid]').val();
    var txt_lazada_apikey = $('input[name=txt_lazada_apikey]').val();

    var $this = $(this);
    var error = "";

    if(validNull('input[name=txt_username]')) {
        $('input[name=txt_username]').removeClass('has-error');
    } else {
        error += "Username không được bỏ trống.\n";
        $('input[name=txt_username]').addClass('has-error');
    }
    if(validNull('input[name=txt_password]')) {
        $('input[name=txt_password]').removeClass('has-error');
    } else {
        error += "Password không được bỏ trống.\n";
        $('input[name=txt_password]').addClass('has-error');
    }
    if(validNull('input[name=txt_lazada_username]')) {
        $('input[name=txt_lazada_username]').removeClass('has-error');
    } else {
        error += "Lazada username không được bỏ trống.\n";
        $('input[name=txt_lazada_username]').addClass('has-error');
    }
    if(validNull('input[name=txt_lazada_userid]')) {
        $('input[name=txt_lazada_userid]').removeClass('has-error');
    } else {
        error += "Lazada userid không được bỏ trống.\n";
        $('input[name=txt_lazada_userid]').addClass('has-error');
    }
    if(validNull('input[name=txt_lazada_apikey]')) {
        $('input[name=txt_lazada_apikey]').removeClass('has-error');
    } else {
        error += "Lazada api key không được bỏ trống.\n";
        $('input[name=txt_lazada_apikey]').addClass('has-error');
    }
    if($('input[name=txt_password]').hasClass('has-error') == false && $('input[name=txt_repassword]').hasClass('has-error') == false) {
        var newpass = ($('input[name=txt_password]').val());
        var repass = ($('input[name=txt_repassword]').val());
        if(repass == newpass) {
            $('input[name=txt_password]').removeClass('has-error');
            $('input[name=txt_repassword]').removeClass('has-error');
        } else {
            error += "Retype passwork và new passwork phải giống nhau.\n";
            $('input[name=txt_password]').addClass('has-error');
            $('input[name=txt_repassword]').addClass('has-error');
        }
    }


    if(error.length > 0) {
        swal("Không hợp lệ", error, "error");
        return;
    }

    var dataType = $('#portlet-user').data('type');
    console.log(dataType);
    if(dataType == "edit")
    {
        $.ajax({
            method:'POST',
            // url: leoz.generateUpdateSkuEndpoind(),
            url: 'http://localhost:5000/user/update',
            contentType: "application/json",
            data: JSON.stringify({
                id: $('input[name=txt_id]').val(),
                username: $('input[name=txt_username]').val(),
                password: $('input[name=txt_password]').val(),
                lazada_username: $('input[name=txt_lazada_username]').val(),
                lazada_userid: $('input[name=txt_lazada_userid]').val(),
                lazada_apikey: $('input[name=txt_lazada_apikey]').val()
            }),
            success: function(data) {
                swal("Success", "", "success");
                $('#portlet-user').modal('hide');
                getAndFillOutAllUser();
            },
            error: function(error) {
                console.log(error);
                var exception = JSON.parse(error.responseText);
                var errorTag = $this.parent().find('.error');
                errorTag.html(exception.error).removeClass('hidden')
            }
        });
    }


    else if (dataType == "insert")
    {
        $.ajax({
            method:'POST',
            // url: leoz.generateInsertSkuEndpoind(),

            url: 'http://localhost:5000/user/insert',
            contentType: "application/json",
            data: JSON.stringify({
                username: $('input[name=txt_username]').val(),
                password: $('input[name=txt_password]').val(),
                lazada_user_name: $('input[name=txt_lazada_username]').val(),
                lazada_user_id: $('input[name=txt_lazada_userid]').val(),
                lazada_api_key: $('input[name=txt_lazada_apikey]').val()
            }),
            success: function(data) {
                swal("Success", "", "success");
                $('#portlet-user').modal('hide');
                getAndFillOutAllUser();
            },
            error: function(error) {
                console.log(error);
                var exception = JSON.parse(error.responseText);
                var errorTag = $this.parent().find('.error');
                errorTag.html(exception.error).removeClass('hidden')
            }
        });
    }

});
//-------------------------------------------------------------------------------------
// Get and fill out all SKU
//-------------------------------------------------------------------------------------
function getAndFillOutAllUser() {
    $.ajax({
        method:'GET',
        // url: leoz.generateGetAllSkuEndpoind(),
        url: 'http://localhost:5000/user/get-all',
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            var template = $("#user-content-template").html();
            var contentHtml = Handlebars.compile(template);
            $("#tbody_sku").html(contentHtml(data));
            enableSwitchery();
        },
        error: function(error) {
            console.log(error);
        }
    });
}

//-------------------------------------------------------------------------------------
// Logout
//-------------------------------------------------------------------------------------
$('#logoutButton').click(function() {
    cookie.clearToken('token');
    cookie.clearToken('myUser');
    window.location.href = "../login";
});
























