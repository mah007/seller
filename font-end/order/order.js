var endpoint    = new EndpointConfig();
var cookie      = new CookieConfig();
var barcodeInput            = $("#barcodeInput");
var submitBarcodeButton     = $("#submitBarcode");
var processLogTitle         = $("#processLogTitle");
var processLogContent       = $("#processLogContent");
var showOrderDetailCheckbox = $("#showOrderDetailCheckbox");

jQuery(document).ready(function() {
    if (!cookie.validateLocalToken()) {
        window.location.href = "../login";
    }

    // Fill user name
    if (cookie.getUsername() === undefined) {
        $('#username-on-header').html("User info");
    } else {
        $('#username-on-header').html(cookie.getUsername());
    }

    // Always request focus for barcode input
    barcodeInput.focus();
});

function refreshLogAndOrder() {
    processLogTitle.html("Log for order number:");
    processLogContent.html("");
    $("#tbody_customer").html("");
    $("#tbody_order-items").html("");
}

//------------------------------------------------------------------------------
// Key shortcuts
//------------------------------------------------------------------------------
$(document).bind('keydown', '0', function() {
    console.log("ok 0");
    barcodeInput.focus();
})
$(document).bind('keydown', '1', function() {
    console.log("ok 1");
    performSubmitBarcode();
})
$(document).bind('keydown', '2', function() {
    console.log("ok 2");
    changeShowOrderDetailCheckbox();
})
$(document).bind('keydown', '3', function() {
    console.log("ok 3");
    performRefreshAllOrders();
})
$(document).bind('keydown', '4', function() {
    console.log("ok 4");
})


$('#barcodeInput').on("keypress", function(e) {
    if (e.keyCode == 13) {  /* ENTER PRESSED*/
        performSubmitBarcode();
    }
});
$("#barcodeInput").keyup(function() {
    var $this = $(this);
    var text = $this.val();
    if (text == '0') {
        $this.val("");
    }
    if (text == '2') {
        changeShowOrderDetailCheckbox();
        $this.val("");
    }
    if (text == '3') {
        performRefreshAllOrders();
        $this.val("");
    }
    if (text == '4') {
        $this.val("");
    }
});

//------------------------------------------------------------------------------
// Show Order detail checkbox
//------------------------------------------------------------------------------
$('#showOrderDetailCheckbox').change(function() {
    if($(this).is(":checked")) {
        $("#orderDetailSection").show();
    } else {
        $("#orderDetailSection").hide();
    }
});

function changeShowOrderDetailCheckbox() {
    if(showOrderDetailCheckbox.is(":checked")) {
        showOrderDetailCheckbox.prop('checked', false);
        $("#orderDetailSection").hide();
    } else {
        showOrderDetailCheckbox.prop('checked', true);
        $("#orderDetailSection").show();
    }
}


//------------------------------------------------------------------------------
// Refesh all orders
//------------------------------------------------------------------------------
$("#getAllOrdersButton").click(function() {
    performRefreshAllOrders
})

function performRefreshAllOrders() {
    var $btn = $("#getAllOrdersButton").button('loading');
    barcodeInput.focus(); // Request focus barcode input again.
    refreshLogAndOrder();

    $.ajax({
        method:'GET',
        url: endpoint.generateRefreshAllOrdersEndPoint(),
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            $btn.button('reset');
            // Fill status
            var template = $("#process-log-success-template").html();
            var contentHtml1 = Handlebars.compile(template);
            processLogContent.html(contentHtml1(data.success));
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
// Scan barcode section
//------------------------------------------------------------------------------
$('#submitBarcode').on('click', function () {
    performSubmitBarcode();
})

function performSubmitBarcode() {
    var $btn = submitBarcodeButton.button('loading');
    var barcode = barcodeInput.val();
    barcodeInput.val(""); // clear barcode input.
    barcodeInput.focus(); // Request focus again.
    refreshLogAndOrder();

    if (barcode == null || barcode == '') {
        $btn.button('reset');
        return;
    }

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
            processLogContent.html(contentHtml1(data.success));
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



























