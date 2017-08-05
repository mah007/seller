var endpoint    = new EndpointConfig();
var cookie      = new CookieConfig();
var barcodeInput        = $("#barcodeInput");
var submitBarcodeButton = $("#submitBarcode");
var processLogTitle     = $("#processLogTitle");
var processLogContent   = $("#processLogContent");

jQuery(document).ready(function() {
    if (!cookie.validateLocalToken()) {
        window.location.href = "../login";
    }

    // Always request focus for barcode input
    barcodeInput.focus();
});


//------------------------------------------------------------------------------
// Scan barcode section
//------------------------------------------------------------------------------
$('#barcodeInput').on("keypress", function(e) {
    if (e.keyCode == 13) {  /* ENTER PRESSED*/
        performSubmitBarcode();
    }
});

$('#submitBarcode').on('click', function () {
    performSubmitBarcode();
})

function performSubmitBarcode() {
    var $btn = submitBarcodeButton.button('loading');
    var barcode = barcodeInput.val();
    barcodeInput.val(""); // clear barcode input.
    barcodeInput.focus(); // Request focus again.

    processLogTitle.html("Log for order number: " + barcode);
    $.ajax({
        method:'POST',
        url: endpoint.generateScanOrderEndPoint(),
        contentType: "application/json",
        data: JSON.stringify({
            barcode: barcode
        }),
        success: function(data) {
            console.log(data);
            $btn.button('reset');
            // Fill status
            var template = $("#process-log-success-template").html();
            var contentHtml1 = Handlebars.compile(template);
            processLogContent.html(contentHtml1(data.data));
            // Fill order
            var orderTemplate = $("#customer-content-template").html();
            var contentHtml2 = Handlebars.compile(orderTemplate);
            $("#tbody_customer").html(contentHtml2(data.data.order));
            // Fill order items
            var orderItemstemplate = $("#order-items-content-template").html();
            var contentHtml3 = Handlebars.compile(orderItemstemplate);
            $("#tbody_order-items").html(contentHtml3(data.data));
        },
        error: function(error) {
            $btn.button('reset');
            console.log(error);
            var exception = JSON.parse(error.responseText);
            var template = $("#process-log-error-template").html();
            var contentHtml = Handlebars.compile(template);
            processLogContent.html(contentHtml(exception));
        }
    });
}


//------------------------------------------------------------------------------
// Get order
//------------------------------------------------------------------------------
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


//------------------------------------------------------------------------------
// Get order item
//------------------------------------------------------------------------------
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


























