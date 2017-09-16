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
    getAndFillOutAllPriceBalancer();

    if($('.btnnew').length > 0) {
        $(".btnnew").click(function() {
            $('#portlet-config').data('type', "insert");
            $('#portlet-config').modal('show');
        });
    }

});


//-------------------------------------------------------------------------------------
// Reload furetures: Edit, Delete, Insert, SwitchSate
//-------------------------------------------------------------------------------------

function enableSwitchery() {

    
    // Delete Sku---------------------------------------------------------------
    if($('.btndel').length > 0) {
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

            }, function () {
                $.ajax({
                    method:'POST',
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
                        }, function () {
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

    // Edit Sku---------------------------------------------------------------
    if($('.btnedt').length > 0) {
        $(".btnedt").click(function() {
            var parent = $(this).parents('tr');
            var id = parent.data('id');
            var name = parent.data('name');
            var sku = parent.data('sku');
            // var repeat_time = parent.data('repeat_time');
            var min_price = parent.data('min_price');
            var max_price = parent.data('max_price');
            var compete_price = parent.data('compete_price');

            $('#portlet-config').data('type', "edit");
            $('#portlet-config .modal-title').html('Chỉnh sửa ' + name);
            $('input[name=id]').val(id);
            $('input[name=txt_sku]').val(sku).prop('disabled', true);
            // $('input[name=txt_seq]').val(repeat_time).prop('disabled', true);
            $('input[name=txt_min]').val(min_price);
            $('input[name=txt_max]').val(max_price);
            $('input[name=txt_stp]').val(compete_price);

            $('#portlet-config').modal('show');
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
$('#portlet-config').on('hidden.bs.modal', function() {
    $('.portlet-config .modal-title').html('Tạo mới');
    $('input[name=txt_act]').val('skucreate');
    $('input[name=txt_sku]').val('');
    $('input[name=txt_min]').val('');
    $('input[name=txt_max]').val('');
    $('input[name=txt_stp]').val('');
    $('input[name=txt_seq]').val('');
    $('select[name=txt_stt]').val('active');
});

//-------------------------------------------------------------------------------------
// Add new SKU
//-------------------------------------------------------------------------------------
$(".btnmodalsubmit").click(function() {
    var txtSku = $('input[name=txtSku]').val();
    var txtName = $('input[name=txtName]').val();
    var txtUrl = $('input[name=txtUrl]').val();
    var txtCurrentPrice = $('input[name=txtCurrentPrice]').val();
    var txtPriceByTime = $('input[name=txtPriceByTime]').val();
    var error = "";
    // if(!validNull('input[name=txtSku]')) {
    //     error += "Seller SKU không được bỏ trống.\n";
    //     $('input[name=txt_sku]').addClass('has-error');
    // }
    // if(validNull('input[name=txt_min]')) {
    //     $('input[name=txt_min]').removeClass('has-error');
    // } else {
    //     error += "Mức giá tối thiểu không được bỏ trống.\n";
    //     $('input[name=txt_min]').addClass('has-error');
    // }
    // if(validNull('input[name=txt_max]')) {
    //     $('input[name=txt_max]').removeClass('has-error');
    // } else {
    //     error += "Mức giá tối đa không được bỏ trống.\n";
    //     $('input[name=txt_max]').addClass('has-error');
    // }
    // if($('input[name=txt_min]').hasClass('has-error') == false && $('input[name=txt_max]').hasClass('has-error') == false) {
    //     var min = parseInt($('input[name=txt_min]').val());
    //     var max = parseInt($('input[name=txt_max]').val());
    //     if(min < max) {
    //         $('input[name=txt_min]').removeClass('has-error');
    //         $('input[name=txt_max]').removeClass('has-error');
    //     } else {
    //         error += "Mức giá tối thiểu phải nhỏ hơn mức giá tối đa.\n";
    //         $('input[name=txt_min]').addClass('has-error');
    //         $('input[name=txt_max]').addClass('has-error');
    //     }
    // }

    if(error.length > 0) {
        swal("Không hợp lệ", error, "error");
        return;
    }

    var dataType = $('#portlet-config').data('type');
    if(dataType == "edit")
    {
        $.ajax({
            method:'POST',
            url: endpoint.generateUpdateSkuEndpoind(),
            contentType: "application/json",
            data: JSON.stringify({
                id: $('input[name=id]').val(),
                sku: $('input[name=txt_sku]').val(),
                min_price: $('input[name=txt_min]').val(),
                max_price: $('input[name=txt_max]').val(),
                compete_price: $('input[name=txt_stp]').val(),
                // repeat_time: $('input[name=txt_seq]').val(),
                state: $('select[name=txt_stt]').val() == "active" ? 1 : 0
            }),
            success: function(data) {
                console.log(data);
                swal("Success", "", "success");
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
    }
    else if (dataType == "insert")
    {
        $.ajax({
            method:'POST',
            url: endpoint.generateInsertPriceBalancer(),
            contentType: "application/json",
            data: JSON.stringify({
                sku: $('input[name=txt_sku]').val(),
                name: $('input[name=txt_min]').val(),
                url: $('input[name=txt_max]').val(),
                current_price: $('input[name=txt_stp]').val(),
                price_by_time: $('select[name=txt_stt]').val()
            }),
            success: function(data) {
                swal("Success", "", "success");
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
    }
});

//-------------------------------------------------------------------------------------
// Get and fill out all price balancer
//-------------------------------------------------------------------------------------
function getAndFillOutAllPriceBalancer() {
    $.ajax({
        method:'GET',
        url: endpoint.generateGetAllPriceBalancer(),
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
