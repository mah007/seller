var endpoint    = new EndpointConfig();
var cookie      = new CookieConfig();
var barcodeInput            = $("#barcodeInput");
var processLogTitle         = $("#processLogTitle");
var processLogContent       = $("#processLogContent");
var showOrderDetailCheckbox = $("#showOrderDetailCheckbox");
var orderItemIds            = $("#orderItemIds");
var shippingProvider        = $("#shippingProvider");

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
    clearAndFocusBarcodeInput();
});

function clearAndFocusBarcodeInput() {
    barcodeInput.val("");
    barcodeInput.focus();
}

function refreshLogAndOrder() {
    processLogTitle.html("Log for order number:");
    processLogContent.html("");
    $("#tbody_customer").html("");
    $("#tbody_order-items").html("");
}

function fillErrorLog(errorArray) {
    var template = $("#process-log-error-template").html();
    var contentHtml = Handlebars.compile(template);
    processLogContent.html(contentHtml(errorArray));
}

function fillSuccessLog(successMessage) {
    var template = $("#process-log-success-template").html();
    var contentHtml = Handlebars.compile(template);
    processLogContent.html(contentHtml(successMessage));
}

//------------------------------------------------------------------------------
// Key shortcuts
//------------------------------------------------------------------------------
$(document).bind('keydown', '0', function() {
    console.log("ok 0");
    clearAndFocusBarcodeInput();
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
    performSetStatusToReadyToShip();
})


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
        performSetStatusToReadyToShip();
    }
});
$('#barcodeInput').on("keypress", function(e) {
    if (e.keyCode == 13) {  /* ENTER PRESSED*/
        performSubmitBarcode();
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
    performRefreshAllOrders();
})

function performRefreshAllOrders() {
    var $btn = $("#getAllOrdersButton").button('loading');
    clearAndFocusBarcodeInput();
    refreshLogAndOrder();

    $.ajax({
        method:'GET',
        url: endpoint.generateRefreshAllOrdersEndPoint(),
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            $btn.button('reset');
            fillSuccessLog(data.success);
        },
        error: function(error) {
            $btn.button('reset');
            console.log(error);
            fillErrorLog(JSON.parse(error.responseText));
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
    var $btn = $("#submitBarcode").button('loading');
    var barcode = barcodeInput.val();
    clearAndFocusBarcodeInput();
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
            fillSuccessLog(data.success);
            // Fill order
            var orderTemplate = $("#customer-content-template").html();
            var contentHtml2 = Handlebars.compile(orderTemplate);
            $("#tbody_customer").html(contentHtml2(data.data.order));
            // Fill order items
            var orderItemstemplate = $("#order-items-content-template").html();
            var contentHtml3 = Handlebars.compile(orderItemstemplate);
            $("#tbody_order-items").html(contentHtml3(data.data));
            // Store orderItemIds
            orderItemIds.html("")
            if (data.data.orderItems.length > 0) {
                $.each(data.data.orderItems, function(key, orderItem) {
                    if (orderItemIds.html() === "" || orderItemIds.html() === null) {
                        orderItemIds.html(orderItem.OrderItemId);
                    } else {
                        orderItemIds.html(orderItemIds.html() + "," + orderItem.OrderItemId);
                    }
                });
            }
            // Store shippingProvider
            shippingProvider.html("");
            if (data.data.orderItems.length > 0) {
                var orderItem = data.data.orderItems[0];
                shippingProvider.html(orderItem.ShipmentProvider)
            }
        },
        error: function(error) {
            $btn.button('reset');
            console.log(error);
            fillErrorLog(JSON.parse(error.responseText));
        }
    });
}


//------------------------------------------------------------------------------
// Set status to ready to ship
//------------------------------------------------------------------------------
$("#readyToShipButton").click(function() {
    performSetStatusToReadyToShip();
})

function performSetStatusToReadyToShip() {
    var $btn = $("#readyToShipButton").button('loading');
    var orderItemIdList = orderItemIds.html();
    var shippingProviderData = shippingProvider.html();

    if (orderItemIdList == null || orderItemIdList == '') {
        $btn.button('reset');
        fillErrorLog(["Can't get orderItem Id list, please scan barcode again fist and try again !"]);
        return;
    }
    if (shippingProviderData == null || shippingProviderData == '') {
        $btn.button('reset');
        fillErrorLog(["Can't get shipping provider, please scan barcode again fist and try again !"]);
        return;
    }

    $.ajax({
        method:'POST',
        url: endpoint.generateSetStatusReadyToShipEndPoint(),
        contentType: "application/json",
        data: JSON.stringify({
            orderItemIds: orderItemIdList,
            shippingProvider: shippingProviderData
        }),
        success: function(data) {
            console.log(data);
            $btn.button('reset');
            fillSuccessLog(data.success);
        },
        error: function(error) {
            $btn.button('reset');
            console.log(error);
            fillErrorLog(JSON.parse(error.responseText));
        }
    });
}





























