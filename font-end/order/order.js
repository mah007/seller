var endpoint = new EndpointConfig();
var cookie = new CookieConfig();

jQuery(document).ready(function() {
    if (!cookie.validateLocalToken()) {
        window.location.href = "../login";
    } else {
        getAndFillOutAllCustomer();
        getAndFillOutAllOrderItems();
    }
});

$('#submitBarcode').on('click', function () {
    var $btn = $(this).button('loading');
    var barcode = $("#barcodeInput").val();
    console.log(barcode);

    $("#processLogTitle").html("Log for order number: " + barcode);
    $.ajax({
        method:'POST',
        url: endpoint.generateScanOrderEndPoint(),
        contentType: "application/json",
        data: JSON.stringify({
            barcode: barcode
        }),
        success: function(data) {
            console.log(data);
            $btn.button('reset')
        },
        error: function(error) {
            console.log(error);
            $btn.button('reset')
        }
    });
})

function getAndFillOutAllCustomer() {
    $.ajax({
        method:'GET',
        url: 'http://localhost:5000/order/get-order',
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            var template = $("#customer-content-template").html();
            var contentHtml = Handlebars.compile(template);
            $("#tbody_customer").html(contentHtml(data));
        },
        error: function(error) {
            console.log(error);
            alert("Sorry! Error occur in process!");
        }
    });
}

function getAndFillOutAllOrderItems() {
    $.ajax({
        method:'GET',
        url: 'http://localhost:5000/order/get-order-items',
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            var template = $("#order-items-content-template").html();
            var contentHtml = Handlebars.compile(template);
            $("#tbody_order-items").html(contentHtml(data));
        },
        error: function(error) {
            console.log(error);
            alert("Sorry! Error occur in process!");
        }
    });
}


























