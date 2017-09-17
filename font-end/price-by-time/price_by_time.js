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

    // Init data
    getAndFillOutAllPriceByTime();
    AutoCompleteSearch();

    // Should focus SKU input
    focusSKUInput();
});

function focusSKUInput() {
    $('input[name=txtSku]').focus();
}



//-------------------------------------------------------------------------------------
// Reload furetures: Edit, Delete, Insert, SwitchSate
//-------------------------------------------------------------------------------------

function enableSwitchery() {
    // Delete price balancer---------------------------------------------------------------
    if ($('.btndel').length > 0) {
        $('.btndel').click(function() {
            var id = $(this).parents('tr').data('id');
            swal({
                title: "Are you sure?",
                text: "You will not be able to recover this Price Balancer!",
                type: "warning",
                showReloadButton: true,
                confirmButtonColor: "#DD6B55",
                cancelButtonColor: '#d33',
                confirmButtonText: "Yes, delete it!",
                closeOnConfirm: false,
                showCancelButton: true,

            }, function() {
                $.ajax({
                    method: 'POST',
                    url: endpoint.generateDeletePriceByTime(),
                    contentType: "application/json",
                    data: JSON.stringify({
                        id: id
                    }),
                    success: function(data) {
                        swal({
                            title: "Deleted!",
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
            });
        });
    }

    // // Edit Sku---------------------------------------------------------------
    // if($('.btnedt').length > 0) {
    //     $(".btnedt").click(function() {
    //         var parent = $(this).parents('tr');
    //         var id = parent.data('id');
    //         var name = parent.data('name');
    //         var sku = parent.data('sku');
    //         // var repeat_time = parent.data('repeat_time');
    //         var min_price = parent.data('min_price');
    //         var max_price = parent.data('max_price');
    //         var compete_price = parent.data('compete_price');

    //         $('#portlet-config').data('type', "edit");
    //         $('#portlet-config .modal-title').html('Chỉnh sửa ' + name);
    //         $('input[name=id]').val(id);
    //         $('input[name=txt_sku]').val(sku).prop('disabled', true);
    //         // $('input[name=txt_seq]').val(repeat_time).prop('disabled', true);
    //         $('input[name=txt_min]').val(min_price);
    //         $('input[name=txt_max]').val(max_price);
    //         $('input[name=txt_stp]').val(compete_price);

    //         $('#portlet-config').modal('show');
    //     });
    // }

}

//-------------------------------------------------------------------------------------
// ???
//-------------------------------------------------------------------------------------
$('#portlet-config').on('hidden.bs.modal', function() {
    $('.portlet-config .modal-title').html('Tạo mới');
    $('input[name=txtSku]').val('');
    $('input[name=txtName]').val('');
    $('input[name=txtUrl]').val('');
    $('input[name=txtCurrentPrice]').val('');
    $('input[name=txtPriceByTime]').val('');
});

//-------------------------------------------------------------------------------------
// Search
//-------------------------------------------------------------------------------------
$("#btnsearch").click(function() {
    $.ajax({
        method: 'POST',
        url: endpoint.generateSearchPriceByTime(),
        contentType: "application/json",
        data: JSON.stringify({
            search_key: $('input[name=txt_search]').val(),
        }),
        success: function(data) {
            console.log(data);
        },
        error: function(error) {
            console.log(error);
            errorLog.html(error);
        }
    });
})
//-------------------------------------------------------------------------------------
// Add new SKU
//-------------------------------------------------------------------------------------
$("#btnAddNew").click(function() {
    var priceByTime = validateAddNewPriceByTimeValues();
    console.log(priceByTime);
    if (!priceByTime) {
        return;
    }

    console.log(priceByTime);
    $.ajax({
        method: 'POST',
        url: endpoint.generateInsertPriceByTime(),
        contentType: "application/json",
        data: JSON.stringify({
            sku: $('input[name=txtSku]').val(),
            price_by_time: priceByTime
        }),
        success: function(data) {
            console.log(data);
            getAndFillOutAllPriceByTime();
        },
        error: function(error) {
            console.log(error);
            errorLog.html(error);
        }
    });
})

function validateAddNewPriceByTimeValues() {
    var txtSku = $('input[name=txtSku]').val();
    if (!txtSku) {
        $('input[name=txtSku]').addClass('has-error');
        console.log("txtSku");
        return false;
    }
    var txtFromHour01 = $('input[name=txtFromHour01]').val();
    if (!txtFromHour01) {
        $('input[name=txtFromHour01]').addClass('has-error');
        console.log("txtFromHour01");
        return false;
    }
    var txtFromMinute01 = $('input[name=txtFromMinute01]').val();
    if (!txtFromMinute01) {
        console.log("txtFromMinute01");
        $('input[name=txtFromMinute01]').addClass('has-error');
        return false;
    }
    var txtPrice01 = $('input[name=txtPrice01]').val();
    if (!txtPrice01) {
        $('input[name=txtPrice01]').addClass('has-error');
        console.log("txtPrice01");
        return false;
    }
    var txtFromHour02 = $('input[name=txtFromHour02]').val();
    if (!txtFromHour02) {
        $('input[name=txtFromHour02]').addClass('has-error');
        return false;
    }
    var txtFromMinute02 = $('input[name=txtFromMinute02]').val();
    if (!txtFromMinute02) {
        $('input[name=txtFromMinute02]').addClass('has-error');
        return false;
    }
    var txtPrice02 = $('input[name=txtPrice02]').val();
    if (!txtPrice02) {
        $('input[name=txtPrice02]').addClass('has-error');
        return false;
    }
    var txtFromHour03 = $('input[name=txtFromHour03]').val();
    if (!txtFromHour03) {
        $('input[name=txtFromHour03]').addClass('has-error');
        return false;
    }
    var txtFromMinute03 = $('input[name=txtFromMinute03]').val();
    if (!txtFromMinute03) {
        $('input[name=txtFromMinute03]').addClass('has-error');
        return false;
    }
    var txtPrice03 = $('input[name=txtPrice03]').val();
    if (!txtPrice03) {
        $('input[name=txtPrice03]').addClass('has-error');
        return false;
    }

    var priceByTime = '[{"from": "{0}:{1}", "price": {2}},' +
        '{"from": "{3}:{4}", "price": {5}},' +
        '{"from": "{6}:{7}", "price": {8}}]';
    priceByTime = priceByTime.format(txtFromHour01, txtFromMinute01, txtPrice01,
        txtFromHour02, txtFromMinute02, txtPrice02,
        txtFromHour03, txtFromMinute03, txtPrice03);
    return priceByTime;
}

//------------------------------------------------------------------------------
// Get and fill out all price balancer
//------------------------------------------------------------------------------
function getAndFillOutAllPriceByTime() {
    $.ajax({
        method: 'GET',
        url: endpoint.generateGetAllPriceByTime(),
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            var template = $("#price-content-template").html();
            var contentHtml = Handlebars.compile(template);
            $("#tbody_price").html(contentHtml(data));
            enableSwitchery();
            focusSKUInput();
        },
        error: function(error) {
            console.log(error);
        }
    });
};

//------------------------------------------------------------------------------
// Additional functions
//------------------------------------------------------------------------------

function validNull(selector) {
    if ($(selector).length > 0) {
        if ($(selector).prop("tagName").toLowerCase() == "select") {
            return ($(selector).val() > 0) ? true : false;
        } else {
            return ($(selector).val().length > 0) ? true : false;
        }
    } else {
        return false;
    }
}

function AutoCompleteSearch() {
    $(function() {
        $('#autocomplete').autoComplete({
            minChars: 1,
            source: function(term, suggest) {
                term = term.toLowerCase();
                var choices = ['ActionScript', 'AppleScript', 'Asp', 'Assembly', 'BASIC', 'Batch', 'C', 'C++', 'CSS', 'Clojure', 'COBOL', 'ColdFusion', 'Erlang', 'Fortran', 'Groovy', 'Haskell', 'HTML', 'Java', 'JavaScript', 'Lisp', 'Perl', 'PHP', 'PowerShell', 'Python', 'Ruby', 'Scala', 'Scheme', 'SQL', 'TeX', 'XML'];
                var suggestions = [];
                for (i = 0; i < choices.length; i++)
                    if (~choices[i].toLowerCase().indexOf(term)) suggestions.push(choices[i]);
                suggest(suggestions);
            }
        });

    });
}

if (!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        var str = this;

        function replaceByObjectProperies(obj) {
            for (var property in obj)
                if (obj.hasOwnProperty(property))
                    //replace all instances case-insensitive
                    str = str.replace(new RegExp(escapeRegExp("{" + property + "}"), 'gi'), String(obj[property]));
        }

        function escapeRegExp(string) {
            return string.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
        }

        function replaceByArray(arrayLike) {
            for (var i = 0, len = arrayLike.length; i < len; i++)
                str = str.replace(new RegExp(escapeRegExp("{" + i + "}"), 'gi'), String(arrayLike[i]));
        }

        if (!arguments.length || arguments[0] === null || arguments[0] === undefined)
            return str;
        else if (arguments.length == 1 && Array.isArray(arguments[0]))
            replaceByArray(arguments[0]);
        else if (arguments.length == 1 && typeof arguments[0] === "object")
            replaceByObjectProperies(arguments[0]);
        else
            replaceByArray(arguments);

        return str;
    };
}

