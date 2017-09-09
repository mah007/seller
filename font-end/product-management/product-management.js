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
    checkFilled();

});

function checkFilled() {
    var inputQuantity = document.getElementById("quantityText");
    var inputPrice = document.getElementById("priceText");
    if (inputQuantity.value == "") {
        inputQuantity.style.backgroundColor = "#efeff5";
    } else {
        inputQuantity.style.backgroundColor = "";
    }
    if (inputPrice.value == "") {
        inputPrice.style.backgroundColor = "#efeff5";
    } else {
        inputPrice.style.backgroundColor = "";
    }
}

checkFilled();
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
            // var template = $("#sku-content-template").html();
            // var contentHtml = Handlebars.compile(template);
            // $("#tbody_sku").html(contentHtml(data));
        },
        error: function(error) {
            console.log(error);
        }
    });
};