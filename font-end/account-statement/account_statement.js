var endpoint = new EndpointConfig();
var cookie = new CookieConfig();
var errorLog = $("#errorLog");

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
    getAndFillOutAllAccountStatement();
    getAndFillOutAllAccountStatementException();

    if ($('.btnUpdate').length > 0) {
        $(".btnUpdate").click(function() {
            var body = document.getElementById("tbody_account-statement");
            var length = body.rows.length;

            for (var i = 0; i < length; i += 1) {
                var row = body.rows[i];

                var id = $(row).data("id");
                var oriPrice = $(row).data("seller_price");

                var price = row.cells[5].children[0].value.replace(/\,/g, '');

                if (oriPirce != price) {
                    updateAccountStatement(price, id);
                }
            }
        });
    }

});

//-------------------------------------------------------------------------------------
// Update Sku
//-------------------------------------------------------------------------------------
function updateProduct(price, id) {
    $.ajax({
        method: 'POST',
        url: endpoint.generateUpdateAccountStatementPrice(),
        contentType: "application/json",
        data: JSON.stringify({
            id: id,
            price: price
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

//-------------------------------------------------------------------------------------
// Get all invoice
//-------------------------------------------------------------------------------------
function getAndFillOutAllAccountStatement() {
    $.ajax({
        method: 'GET',
        url: endpoint.generateGetAllAccountStatement(),
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            var template = $("#account-content-template").html();
            var contentHtml = Handlebars.compile(template);
            $("#tbody_account-statement").html(contentHtml(data));
        },
        error: function(error) {
            console.log(error);
        }
    });
}

//-------------------------------------------------------------------------------------
// Get all invoice
//-------------------------------------------------------------------------------------
function getAndFillOutAllAccountStatementException() {
    $.ajax({
        method: 'GET',
        url: endpoint.generateGetAllAccountStatementException(),
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            var template = $("#exception-content-template").html();
            var contentHtml = Handlebars.compile(template);
            $("#tbody_exception").html(contentHtml(data));
        },
        error: function(error) {
            console.log(error);
        }
    });
}