var endpoint = new EndpointConfig();
var cookie = new CookieConfig();
var additional = new Additional();
var errorLog = $("#errorLog");
var $income = $("#income");
var $salesRevenue = $("#sales_revenue");

jQuery(document).ready(function() {
    // Validate Token
    if (!cookie.validateLocalToken()) {
        window.location.href = "../login";
    }
    // Load header
    $("#header_content").load("../header.html");

    // Fill Account statement data
    getAndFillOutAllAccountStatement();
});

function getAndFillOutAllAccountStatement() {
    $.ajax({
        method: 'GET',
        url: endpoint.generateGetAccountStatements(),
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            var template = $("#datetime-template").html();
            var contentHtml = Handlebars.compile(template);
            $("#account_statement_datetime").html(contentHtml(data))
                                            .change();
        },
        error: function(error) {
            console.log(error);
        }
    });
}

//------------------------------------------------------------------------------
// Show/hide statement error info
//------------------------------------------------------------------------------
$("#checkbox_statement_errors").change(function() {
    if($(this).is(":checked")) {
        $("#account_statement_error").hide()
    } else {
        $("#account_statement_error").show()
    }
})

//------------------------------------------------------------------------------
// Get data from Account Statement dropdown selected changed
//------------------------------------------------------------------------------
$("#account_statement_datetime").change(function() {
    var selectedItem = $(this).find(':selected');
    var income = selectedItem.attr('data-income')
    var saleRevenue = selectedItem.attr('data-sales-revenue')
    var accountStatementId = selectedItem.val();

    $income.html(additional.formatMoney(income) + " VND");
    $salesRevenue.html(additional.formatMoney(saleRevenue) + " VND");
    getAccountStatementInfo(accountStatementId);
});

function getAccountStatementInfo(accountStatementId) {
    $.ajax({
        method: 'POST',
        url: endpoint.generateGetAccountStatementInfo(),
        contentType: "application/json",
        data: JSON.stringify({
            account_statement_id: accountStatementId
        }),
        success: function(response) {
            console.log(response);
            // Fill exception data
            var template = $("#exception-content-template").html();
            var contentHtml = Handlebars.compile(template);
            $("#tbody_exception").html(contentHtml(response.data));
            // Fill order items
            var template = $("#product-template").html();
            var contentHtml = Handlebars.compile(template);
            $("#tbody_order_items").html(contentHtml(response.data));
            // Init Money Input
            additional.initMoneyInput();
        },
        error: function(error) {
            console.log(error);
        }
    });
}

//------------------------------------------------------------------------------
// Update OrderItem original price
//------------------------------------------------------------------------------
$(".btnUpdate").click(function() {
    var body = document.getElementById("tbody_order_items");
    var length = body.rows.length;
    var orderItems = []
    for (var i = 0; i < length; i += 1) {
        var row = body.rows[i];

        var shopSku = $(row).data("shop-sku");
        var curPrice = $(row).data("original-price");
        var newPrice = $(row).find('input').val();
        var orderItemId = $(row).data("order-item-id");
        var orderId = $(row).data("order-id");
        if (curPrice != newPrice) {
            orderItems.push({
                "order_id": orderId,
                "order_item_id": orderItemId,
                "original_price": parseInt(newPrice.replace(/\,/g, "")),
                "shop_sku": shopSku,
            });
        }
    }

    if (orderItems.length > 0) {
        updateOrginalPriceAndReComputeIncome(orderItems);
    }
});

function updateOrginalPriceAndReComputeIncome(orderItems) {
    accountStatementId = $("#account_statement_datetime").find(':selected').val();
    $.ajax({
        method: 'POST',
        url: endpoint.getUpdateOriginPriceUrl(),
        contentType: "application/json",
        data: JSON.stringify({
            order_items: orderItems,
            account_statement_id: parseInt(accountStatementId)
        }, null, 2),
        success: function(data) {
            swal({
                title: "Update Successfully!",
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
}








