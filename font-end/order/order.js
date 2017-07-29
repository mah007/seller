var endpoint = new EndpointConfig();

jQuery(document).ready(function() {
    // Init data
    getAndFillOutAllCustomer();


});

//-------------------------------------------------------------------------------------
// Get and fill out all User
//-------------------------------------------------------------------------------------
function getAndFillOutAllCustomer() {
    $.ajax({
        method:'GET',
        url: 'http://localhost:5000/sku/get-order',
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            console.log(data[0].CreatedAt);
            console.log(data[0].AddressBilling.Address1);

            var template = $("#customer-content-template").html();
            var contentHtml = Handlebars.compile(template);
            $("#tbody_customer").html(contentHtml(data[0]));
        },
        error: function(error) {
            console.log(error);
            alert("Sorry! Error occur in process!");
        }
    });
}


























