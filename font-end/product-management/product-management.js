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

    if($('.btnUpdate').length > 0) {
        $(".btnUpdate").click(function() {
            console.log("Update");        
        });
    }

});



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