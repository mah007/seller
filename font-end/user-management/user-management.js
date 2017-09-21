var endpoint = new EndpointConfig();
var cookie = new CookieConfig();

jQuery(document).ready(function() {

    // Validate Token
    if (!cookie.validateLocalToken()) {
        window.location.href = "../login";
    }

    // Fill user name
    if (cookie.getUsername() === undefined) {
        $('#username-on-header').html("User info");
    } else {
        $('#username-on-header').html(cookie.getUsername());
    }

    // Load menu left
    $("#menuContent").load("../menuleft.html");

    // Init data
    getAndFillOutAllUser();

    if($('.btnnew').length > 0) {
        $(".btnnew").click(function() {
            $('#portlet-user .modal-title').html('Thêm mới');
            $('#portlet-user').data('type', "insert");
            $('input[name=txt_id').prop('disabled', true);
            $('input[name=txt_username]').prop('disabled', false);
            $('#portlet-user').modal('show');

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
                cancelButtonColor: '#d33',
                confirmButtonText: "Yes, delete it!",
                closeOnConfirm: false,
                showCancelButton: true,
            }, function () {
                $.ajax({
                    method:'POST',
                    url: endpoint.generateDeleteUserEndpoind(),
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
                            window.location.href = "";
                        });
                    },
                    error: function(error) {
                        console.log(error);
                        swal({
                            title: "Don't Have Permission!",
                            text: "",
                            type: "error",
                            confirmButtonText: "Understand",
                        });
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
            var certain_size = parent.data('certain_size');

            $('#portlet-user').data('type', "edit");
            $('#portlet-user .modal-title').html('Chỉnh sửa ' + username);
            $('input[name=txt_id').val(id).prop('disabled', true);
            $('input[name=txt_username]').val(username).prop('disabled', true);
            $('input[name=txt_lazada_username]').val(lazada_username);
            $('input[name=txt_lazada_userid]').val(lazada_userid);
            $('input[name=txt_lazada_apikey]').val(lazada_apikey);
            $('input[name=txt_certain_size]').val(certain_size);

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
//-------------------------------------------------------------------------------------
// ???
//-------------------------------------------------------------------------------------
$('#portlet-user').on('hidden.bs.modal', function() {
    $('.portlet-user .modal-title').html('Tạo mới');
    $('#portlet-user').data('type', "");
    $('input[name=txt_username]').val('');
    $('input[name=txt_password]').val('');
    $('input[name=txt_repassword]').val('');
    $('input[name=txt_lazada_username]').val('');
    $('input[name=txt_lazada_userid]').val('');
    $('input[name=txt_lazada_apikey]').val('');
    $('input[name=txt_certain_size]').val('');
});

$(".btnmodalsubmit").click(function() {
    var txt_username = $('input[name=txt_username]').val();
    var txt_password = $('input[name=txt_password]').val();
    var txt_lazada_username = $('input[name=txt_lazada_username]').val();
    var txt_lazada_userid = $('input[name=txt_lazada_userid]').val();
    var txt_lazada_apikey = $('input[name=txt_lazada_apikey]').val();
    var txt_certain_size = $('input[name=txt_certain_size]').val();

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
    if(validNull('input[name=txt_certain_size]')) {
        $('input[name=txt_certain_size]').removeClass('has-error');
    } else {
        error += "Lazada api key không được bỏ trống.\n";
        $('input[name=txt_certain_size]').addClass('has-error');
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
            url: endpoint.generateUpdateUserEndpoind(),
            contentType: "application/json",
            data: JSON.stringify({
                id: $('input[name=txt_id]').val(),
                username: $('input[name=txt_username]').val(),
                password: $('input[name=txt_password]').val(),
                lazada_username: $('input[name=txt_lazada_username]').val(),
                lazada_userid: $('input[name=txt_lazada_userid]').val(),
                lazada_apikey: $('input[name=txt_lazada_apikey]').val(),
                certain_size: $('input[name=txt_certain_size]').val()
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
            url: endpoint.generateInsertUserEndpoind(),
            contentType: "application/json",
            data: JSON.stringify({
                username: $('input[name=txt_username]').val(),
                password: $('input[name=txt_password]').val(),
                lazada_user_name: $('input[name=txt_lazada_username]').val(),
                lazada_user_id: $('input[name=txt_lazada_userid]').val(),
                lazada_api_key: $('input[name=txt_lazada_apikey]').val(),
                certain_size: $('input[name=txt_certain_size]').val(),
                role: $('select[name=txt_role]').val() == "active" ? 1 : 0
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
// Get and fill out all User
//-------------------------------------------------------------------------------------
function getAndFillOutAllUser() {
    $.ajax({
        method:'GET',
        url: endpoint.generateGetAllUserEndpoind(),
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            var template = $("#user-content-template").html();
            var contentHtml = Handlebars.compile(template);
            $("#tbody_sku").html(contentHtml(data));

            $('input[name=txt_id]').val('').prop('disabled', false);
            $('input[name=txt_username]').prop('disabled', false);
            enableSwitchery();
        },
        error: function(error) {
            console.log(error);
            alert("Sorry! You don't have permission to access this page!");
            window.location.href = "../sku-management";
        }
    });
}
























