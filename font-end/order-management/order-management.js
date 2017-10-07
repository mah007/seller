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
    // $("#menuContent").load("../menuleft.html");
    $("#header_content").load("../header.html");

    if ($('.btnrefresh').length > 0) {
        $(".btnrefresh").click(function() {
            $.ajax({
                method: 'GET',
                url: endpoint.generateGetFailedOrders(),
                contentType: "application/json",
                success: function(data) {
                    // console.log(data);
                    swal({
                        title: "Refresh thành công!",
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
    }

    // Init data
    getAndFillOutAllOrder();

});

function enableSwitchery() {

    // Update state---------------------------------------------------------------------
    if ($('.btnstatus').length > 0) {
        var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch'));
        elems.forEach(function(html) {
            var switchery = new Switchery(html);
        });
        $('.btnstatus').change(function() {
            var id = $(this).parents('tr').data('id');
            var _parent = $(this).parents("tr");
            $.ajax({
                method: 'POST',
                url: endpoint.generateUpdateOrderState(),
                contentType: "application/json",
                data: JSON.stringify({
                    id: id,
                }),
                success: function(data) {
                    swal({
                        title: "Trạng thái đã được cập nhật!",
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
    }

}

function getAndFillOutAllOrder() {
    $.ajax({
        method: 'GET',
        url: endpoint.generateGetFailedOrders(),
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            var template = $("#order-content-template").html();
            var contentHtml = Handlebars.compile(template);
            $("#tbody_order").html(contentHtml(data));

            enableSwitchery();
        },
        error: function(error) {
            console.log(error);
            // alert("Sorry! You don't have permission to access this page!");
            // window.location.href = "../sku-management";
        }
    });
}

