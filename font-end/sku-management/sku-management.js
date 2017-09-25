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
    getAndFillOutAllSku();
    getAndFillOutHistory();
    // getAndFillOutAllPriceByTime();

    if ($('.btnstt').length > 0) {
        $(".btnstt").each(function() {
            if ($(this).data("bit") == 'active') {
                $(this).find(".bit-like").addClass("green");
            } else {
                $(this).find(".bit-nope").addClass("red");
            }
        });

        $(".btnstt .bit-like").click(function() {
            var id = $(this).parents('tr').data('id');
            if (!$(this).hasClass("green")) {
                var _this = $(this);
                var _parent = $(this).parents("tr");
                $.ajax({
                    url: "?act=skustatus&id=" + id + "&s=" + $(this).data("bit"),
                    method: "POST",
                    success: function(data) {
                        if (data == -1) {
                            swal("Record " + $(_parent).data("id"), "Update status failure.\n Bạn đã kích hoạt vượt qua số lượng SKU cho phép", "warning");
                        } else if (data) {
                            $(_this).addClass("green").siblings().removeClass("red").parent().data("bit", $(_this).data("bit"));
                            swal("Record " + $(_parent).data("id"), "Status changed to Active", "success");
                        } else {
                            swal("Record " + $(_parent).data("id"), "Update status failure", "error");
                        }
                    }
                });
            }
        });
        $(".btnstt .bit-nope").click(function() {
            var id = $(this).parents('tr').data('id');
            if (!$(this).hasClass("red")) {
                var _this = $(this);
                var _parent = $(this).parents("tr");
                $.ajax({
                    url: "?act=skustatus&id=" + id + "&s=" + $(this).data("bit"),
                    method: "POST",
                    success: function(data) {
                        if (data) {
                            $(_this).addClass("red").siblings().removeClass("green").parent().data("bit", $(_this).data("bit"));
                            swal("Record " + $(_parent).data("id"), "Status changed to Deactive", "success");
                        } else {
                            swal("Record " + $(_parent).data("id"), "Update status failure", "error");
                        }
                    }
                });
            }
        });
    }

    if ($('.sltfiltersku').length > 0) {
        $('.sltfiltersku').change(function() {
            $(this).parents('form').submit();
        });
    }
});


//-------------------------------------------------------------------------------------
// Reload furetures: Edit, Delete, Insert, SwitchSate
//-------------------------------------------------------------------------------------

function enableSwitchery() {

    // Update state-------------------------------------------------------------
    if ($('.btnstatus').length > 0) {
        var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch'));
        elems.forEach(function(html) {
            var switchery = new Switchery(html);
        });
        $('.btnstatus').change(function() {
            var id = $(this).parents('tr').data('id');
            var _parent = $(this).parents("tr");
            var status = 0; // deactive
            if ($(this).is(':checked')) {
                status = 1; // active
            }
            $.ajax({
                method: 'POST',
                url: endpoint.generateUpdateStateSkuEndpoind(),
                contentType: "application/json",
                data: JSON.stringify({
                    id: id,
                    state: status
                }),
                success: function(data) {
                    swal("Record " + $(_parent).data("id"), "Trạng thái đã được cập nhập", "success");
                },
                error: function(error) {
                    console.log(error);
                }
            });
        });
    }

    // Delete Sku---------------------------------------------------------------
    if ($('.btndel').length > 0) {
        $('.btndel').click(function() {
            var id = $(this).parents('tr').data('id');
            swal({
                title: "Are you sure?",
                text: "You will not be able to recover this SKU!",
                type: "warning",
                showReloadButton: true,
                confirmButtonColor: "#DD6B55",
                cancelButtonColor: '#d33',
                confirmButtonText: "Yes, delete it!",
                closeOnConfirm: false,
                showCancelButton: true,

            }, function() {
                $.ajax({
                    method: 'POST',
                    url: endpoint.generateDeleteSkuEndpoind(),
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
                        }, function() {
                            window.location.href = "";
                        });
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            });
        });
    }

    // Edit Sku
    if ($('.btnedt').length > 0) {
        $(".btnedt").click(function() {
            var parent = $(this).parents('tr');
            var id = parent.data('id');
            var name = parent.data('name');
            var sku = parent.data('sku');
            var min_price = parent.data('min_price');
            var max_price = parent.data('max_price');
            var compete_price = parent.data('compete_price');

            $('input[name=txt_id]').val(id);
            $('input[name=txt_sku]').val(sku).prop('disabled', true);
            $('input[name=txt_min]').val(min_price);
            $('input[name=txt_max]').val(max_price);
            $('input[name=txt_stp]').val(compete_price);
        });
    }

}

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

// Update user password
$(".btnupdatePw").click(function() {
    var txt_oldpass = $('input[name=txt_oldpass]').val();
    var txt_newpass = $('input[name=txt_newpass]').val();
    var txt_repass = $('input[name=txt_repass]').val();

    var $this = $(this);
    var error = "";


    if ($('input[name=txt_newpass]').hasClass('has-error') == false && $('input[name=txt_repass]').hasClass('has-error') == false) {
        var newpass = ($('input[name=txt_newpass]').val());
        var repass = ($('input[name=txt_repass]').val());
        if (repass == newpass) {
            $('input[name=txt_repass]').removeClass('has-error');
            $('input[name=txt_newpass]').removeClass('has-error');
        } else {
            error += "Retype passwork và new passwork phải giống nhau.\n";
            $('input[name=txt_repass]').addClass('has-error');
            $('input[name=txt_newpass]').addClass('has-error');
        }
    }
    if ($('input[name=txt_newpass]').hasClass('has-error') == false && $('input[name=txt_oldpass]').hasClass('has-error') == false) {
        var newpass = ($('input[name=txt_newpass]').val());
        var oldpass = ($('input[name=txt_oldpass]').val());
        if (oldpass != newpass) {
            $('input[name=txt_newpass]').removeClass('has-error');
            $('input[name=txt_oldpass]').removeClass('has-error');
        } else {
            error += "Old passwork và new passwork phải khác nhau.\n";
            $('input[name=txt_newpass]').addClass('has-error');
            $('input[name=txt_oldpass]').addClass('has-error');
        }
    }
    if (validNull('input[name=txt_oldpass]')) {
        $('input[name=txt_oldpass]').removeClass('has-error');
    } else {
        error += "Old password không được bỏ trống.\n";
        $('input[name=txt_oldpass]').addClass('has-error');
    }
    if (validNull('input[name=txt_newpass]')) {
        $('input[name=txt_newpass]').removeClass('has-error');
    } else {
        error += "New password không được bỏ trống.\n";
        $('input[name=txt_newpass]').addClass('has-error');
    }
    if (validNull('input[name=txt_repass]')) {
        $('input[name=txt_repass]').removeClass('has-error');
    } else {
        error += "Retype password không được bỏ trống.\n";
        $('input[name=txt_repass]').addClass('has-error');
    }


    if (error.length > 0) {
        swal("Không hợp lệ", error, "error");
        return;
    }

    var dataType = $('#portlet-updatePw').data('type');
    if (dataType == "updatePw") {
        $.ajax({
            method: 'POST',
            url: endpoint.generateUpdateUserPwEndpoind(),
            contentType: "application/json",
            data: JSON.stringify({
                oldpass: $('input[name=txt_oldpass]').val(),
                newpass: $('input[name=txt_newpass]').val(),
                // token: cookie.getToken()
            }),
            success: function(data) {
                console.log(data);
                swal("Success", "", "success");
                $('#portlet-updatePw').modal('hide');
                getAndFillOutAllSku();
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
// Add new SKU
//-------------------------------------------------------------------------------------
$("#btnAddNew").click(function() {
    var txt_sku = $('input[name=txt_sku]').val();
    var txt_min = $('input[name=txt_min]').val();
    var txt_max = $('input[name=txt_max]').val();
    var txt_stp = $('input[name=txt_stp]').val();
    var txt_seq = $('input[name=txt_seq]').val();
    var $this = $(this);
    var error = "";

    // Check value of input
    if (!validNull('input[name=txt_sku]')) {
        error += "Seller SKU không được bỏ trống.\n";
        $('input[name=txt_sku]').addClass('has-error');
    }
    if (validNull('input[name=txt_min]')) {
        $('input[name=txt_min]').removeClass('has-error');
    } else {
        error += "Mức giá tối thiểu không được bỏ trống.\n";
        $('input[name=txt_min]').addClass('has-error');
    }
    if (validNull('input[name=txt_max]')) {
        $('input[name=txt_max]').removeClass('has-error');
    } else {
        error += "Mức giá tối đa không được bỏ trống.\n";
        $('input[name=txt_max]').addClass('has-error');
    }
    if ($('input[name=txt_min]').hasClass('has-error') == false && $('input[name=txt_max]').hasClass('has-error') == false) {
        var min = parseInt($('input[name=txt_min]').val());
        var max = parseInt($('input[name=txt_max]').val());
        if (min < max) {
            $('input[name=txt_min]').removeClass('has-error');
            $('input[name=txt_max]').removeClass('has-error');
        } else {
            error += "Mức giá tối thiểu phải nhỏ hơn mức giá tối đa.\n";
            $('input[name=txt_min]').addClass('has-error');
            $('input[name=txt_max]').addClass('has-error');
        }
    }
    if (validNull('input[name=txt_stp]')) {
        $('input[name=txt_stp]').removeClass('has-error');
    } else {
        error += "Mức giá thấp hơn đối thủ không được bỏ trống.\n";
        $('input[name=txt_stp]').addClass('has-error');
    }

    // Print error and return if error occur
    if (error.length > 0) {
        swal("Không hợp lệ", error, "error");
        return;
    }

    // Processing insert new sku
    $.ajax({
        method: 'POST',
        url: endpoint.generateInsertSkuEndpoind(),
        contentType: "application/json",
        data: JSON.stringify({
            sku: $('input[name=txt_sku]').val(),
            min_price: $('input[name=txt_min]').val(),
            max_price: $('input[name=txt_max]').val(),
            compete_price: $('input[name=txt_stp]').val(),
            state: $('select[name=txt_stt]').val() == "active" ? 1 : 0
        }),
        success: function(data) {
            $('#portlet-config').modal('hide');
            getAndFillOutAllSku();
        },
        error: function(error) {
            console.log(error);
            var exception = JSON.parse(error.responseText);
            var errorTag = $this.parent().find('.error');
            errorTag.html(exception.error).removeClass('hidden')
        }
    });

});

//-------------------------------------------------------------------------------------
// Update Sku
//-------------------------------------------------------------------------------------
$("#btnUpdate").click(function() {
    var txt_id = $('input[name=txt_id]').val();
    var txt_sku = $('input[name=txt_sku]').val();
    var txt_min = $('input[name=txt_min]').val();
    var txt_max = $('input[name=txt_max]').val();
    var txt_stp = $('input[name=txt_stp]').val();
    var $this = $(this);
    var error = "";

    // Check value of input
    if (!validNull('input[name=txt_sku]')) {
        error += "Seller SKU không được bỏ trống.\n";
        $('input[name=txt_sku]').addClass('has-error');
    }
    if (validNull('input[name=txt_min]')) {
        $('input[name=txt_min]').removeClass('has-error');
    } else {
        error += "Mức giá tối thiểu không được bỏ trống.\n";
        $('input[name=txt_min]').addClass('has-error');
    }
    if (validNull('input[name=txt_max]')) {
        $('input[name=txt_max]').removeClass('has-error');
    } else {
        error += "Mức giá tối đa không được bỏ trống.\n";
        $('input[name=txt_max]').addClass('has-error');
    }
    if ($('input[name=txt_min]').hasClass('has-error') == false && $('input[name=txt_max]').hasClass('has-error') == false) {
        var min = parseInt($('input[name=txt_min]').val());
        var max = parseInt($('input[name=txt_max]').val());
        if (min < max) {
            $('input[name=txt_min]').removeClass('has-error');
            $('input[name=txt_max]').removeClass('has-error');
        } else {
            error += "Mức giá tối thiểu phải nhỏ hơn mức giá tối đa.\n";
            $('input[name=txt_min]').addClass('has-error');
            $('input[name=txt_max]').addClass('has-error');
        }
    }
    if (validNull('input[name=txt_stp]')) {
        $('input[name=txt_stp]').removeClass('has-error');
    } else {
        error += "Mức giá thấp hơn đối thủ không được bỏ trống.\n";
        $('input[name=txt_stp]').addClass('has-error');
    }

    // Print error and return if error occur
    if (error.length > 0) {
        swal("Không hợp lệ", error, "error");
        return;
    }

    // Processing insert new sku
    $.ajax({
        method: 'POST',
        url: endpoint.generateUpdateSkuEndpoind(),
        contentType: "application/json",
        data: JSON.stringify({
            id: $('input[name=txt_id]').val(),
            sku: $('input[name=txt_sku]').val(),
            min_price: $('input[name=txt_min]').val(),
            max_price: $('input[name=txt_max]').val(),
            compete_price: $('input[name=txt_stp]').val(),
            state: $('select[name=txt_stt]').val() == "active" ? 1 : 0
        }),
        success: function(data) {
            getAndFillOutAllSku();
        },
        error: function(error) {
            console.log(error);
            var exception = JSON.parse(error.responseText);
            var errorTag = $this.parent().find('.error');
            errorTag.html(exception.error).removeClass('hidden')
        }
    });

});

//-------------------------------------------------------------------------------------
// Get and fill out all SKU
//-------------------------------------------------------------------------------------
function getAndFillOutAllSku() {
    $.ajax({
        method: 'GET',
        url: endpoint.generateGetAllSkuEndpoind(),
        contentType: "application/json",
        success: function(data) {
            console.log(data.data);
            var template = $("#sku-content-template").html();
            var contentHtml = Handlebars.compile(template);
            $("#tbody_sku").html(contentHtml(data));
            enableSwitchery();
        },
        error: function(error) {
            console.log(error);
        }
    });
};

function getAndFillOutHistory() {
    $.ajax({
        method: 'GET',
        url: endpoint.generateGetHistory(),
        contentType: "application/json",
        success: function(data) {
            console.log(data.data);
            if (data.data.length != 0) {
                var template = $("#history-content-template").html();
                var contentHtml = Handlebars.compile(template);
                $("#tbody_history").html(contentHtml(data));
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
};

//-------------------------------------------------------------------------------------
// Update Password
//-------------------------------------------------------------------------------------
$('#updatePwButton').click(function() {
    $('#portlet-updatePw').data('type', "updatePw");
    $('#portlet-updatePw').modal('show');
});