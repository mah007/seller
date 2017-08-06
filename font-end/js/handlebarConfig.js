Handlebars.registerHelper('ifStatusNotPending', function(status, options) {
  if(status !== "pending") {
    return options.fn(this);
  }
});