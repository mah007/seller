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

    // Init data
    getAndFillOutAllOrder();

});

function enableSwitchery() {

    // Update state---------------------------------------------------------------------
    if($('.btnstatus').length > 0) {
        var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch'));
        elems.forEach(function(html) {
            var switchery = new Switchery(html);
        });
        $('.btnstatus').change(function() {
            var id = $(this).parents('tr').data('Id');
            var _parent = $(this).parents("tr");
            $.ajax({
                method:'POST',
                url: endpoint.generateUpdateOrderState(),
                contentType: "application/json",
                data: JSON.stringify({
                    id: id,
                }),
                success: function (data) {
                    swal("Record " + $(_parent).data("Id"), "Trạng thái đã được cập nhập", "success");
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
        method:'GET',
        url: endpoint.generateGetAllOrders(),
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

























