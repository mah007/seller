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

    // Fill user name
    if (cookie.getUsername() === undefined) {
        $('#username-on-header').html("User info");
    } else {
        $('#username-on-header').html(cookie.getUsername());
    }

    // Load menu left
    $("#menuContent").load("../menuleft.html");

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
            // Fill products
            var template = $("#product-template").html();
            var contentHtml = Handlebars.compile(template);
            $("#tbody_product").html(contentHtml(response.data));
        },
        error: function(error) {
            console.log(error);
        }
    });
}

//------------------------------------------------------------------------------
// Update Product purchase price
//------------------------------------------------------------------------------
$(".btnUpdate").click(function() {
    var body = document.getElementById("tbody_account_statement");
    var length = body.rows.length;

    for (var i = 0; i < length; i += 1) {
        var row = body.rows[i];

        var id = $(row).data("id");
        var shop_sku = $(row).data("shop_sku");
        var oriPrice = $(row).data("item_price");
        var excel_url = $(row).data("excel_url");

        var price = row.cells[5].children[0].value.replace(/\,/g, '');

        if (oriPrice != price) {
            updateAccountStatement(price, id, shop_sku, excel_url);
        }
    }
});

function updateAccountStatement(price, id, shop_sku, excel_url) {

    $.ajax({
        method: 'POST',
        url: endpoint.generateUpdateAccountStatementPrice(),
        contentType: "application/json",
        data: JSON.stringify({
            id: id,
            price: price,
            shop_sku: shop_sku,
            excel_url: excel_url,
        }),
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








