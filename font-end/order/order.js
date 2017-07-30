var endpoint = new EndpointConfig();

jQuery(document).ready(function() {
    // Init data
    getAndFillOutAllCustomer();
    getAndFillOutAllOrderItems();


});

//-------------------------------------------------------------------------------------
// Get and fill out all User
//-------------------------------------------------------------------------------------
function getAndFillOutAllCustomer() {
    $.ajax({
        method:'GET',
        url: 'http://localhost:5000/order/get-order',
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            // console.log(data.data[0].CreatedAt);
            // console.log(data.data[0].AddressBilling.Address1);

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

function getAndFillOutAllOrderItems() {
    $.ajax({
        method:'GET',
        url: 'http://localhost:5000/order/get-order-items',
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            // console.log(data.data[0].CreatedAt);
            // console.log(data.data[0].AddressBilling.Address1);

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


























