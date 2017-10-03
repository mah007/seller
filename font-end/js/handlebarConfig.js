Handlebars.registerHelper('ifStatusNotPending', function(status, options) {
  if(status !== "pending") {
    return options.fn(this);
  }
});

Handlebars.registerHelper('formatCurrency', function(value) {
    return value.toString().replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",");
});