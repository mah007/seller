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
    getAndFillOutProduct();

    if ($('.btnUpdate').length > 0) {
        $(".btnUpdate").click(function() {
            var body = document.getElementById("tbody_product");
            var length = body.rows.length;

            for (var i = 0; i < length; i += 1) {
                var row = body.rows[i];

                var id = $(row).data("id");
                var oriQuantity = $(row).data("quantity");
                var oriPrice = $(row).data("price");

                var quantity = row.cells[10].children[0].value;
                var price = row.cells[12].children[0].value;

                if (oriQuantity != quantity && oriPrice != price) {
                    console.log("Should Update Product");
                    updateProduct(quantity, price, id);
                }
                else if (oriPrice != price) {
                    console.log("Shoud Update Price")
                } 
                else if (oriQuantity != quantity) {
                    console.log("Dont Update");
                }
            }
        });
    }

});


//-------------------------------------------------------------------------------------
// Update product for new quantity and new price
//-------------------------------------------------------------------------------------
function updateProduct(quantity, price, id) {
    $.ajax({
        method: 'POST',
        url: endpoint.generateUpdateProduct(),
        contentType: "application/json",
        data: JSON.stringify({
            id: id,
            quantity: quantity,
            price: price
        }),
        success: function(data) {
            console.log("Update success");
        },
        error: function(error) {
            console.log(error);
        }
    });
}

//-------------------------------------------------------------------------------------
// Update price
//-------------------------------------------------------------------------------------
function updatePrice(price, id) {
    $.ajax({
        method: 'POST',
        url: endpoint.generateUpdateProduct(),
        contentType: "application/json",
        data: JSON.stringify({
            id: id,
            quantity: quantity,
            price: price
        }),
        success: function(data) {
            console.log("Update success");
        },
        error: function(error) {
            console.log(error);
        }
    });
}

//-------------------------------------------------------------------------------------
// Update quantity
//-------------------------------------------------------------------------------------
function updateQuantity(quantity, id) {
    $.ajax({
        method: 'POST',
        url: endpoint.generateUpdateProduct(),
        contentType: "application/json",
        data: JSON.stringify({
            id: id,
            quantity: quantity,
            price: price
        }),
        success: function(data) {
            console.log("Update success");
        },
        error: function(error) {
            console.log(error);
        }
    });
}
//-------------------------------------------------------------------------------------
// Get and fill out all Product
//-------------------------------------------------------------------------------------
function getAndFillOutProduct() {
    $.ajax({
        method: 'GET',
        url: endpoint.generateGetAllProduct(),
        contentType: "application/json",
        success: function(data) {
            console.log(data.data);
            var template = $("#product-content-template").html();
            var contentHtml = Handlebars.compile(template);
            $("#tbody_product").html(contentHtml(data));
        },
        error: function(error) {
            console.log(error);
        }
    });
};