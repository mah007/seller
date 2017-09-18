//------------------------------------------------------------------------------
// Price By Time Autocomplete
//------------------------------------------------------------------------------

var $autocomplete = $('#autocomplete');
var autocompleteData = [
    // AutoComplete data will be null for first time the page loaded
    // Example data: {
    //   value: sellerSku + name,
    //   sellerSku: afasfs,
    //   icon: "http://vn-live-02.slatic.net/p/5/son-tay-te-bao-chet-cho-moi-duong-moi-beauty-treats-lip-scrub-105ghuong-vanilla-5827-62407031-be699508ded01290b66cb2155a78759c-catalog.jpg",
    //   specialPrice: 14124,
    //   name: name
    // }
];

// Should select all text when click into search input
var $searchInput = $('input[name=search_key]');
$searchInput.click(function () {
   $(this).select();
});

//------------------------------------------------------------------------------
// Init AutoComplete
//------------------------------------------------------------------------------
$autocomplete.autocomplete({
    minLength: 0,
    source: autocompleteData,
    focus: function( event, ui ) {
        console.log("focus");
        $autocomplete.val( ui.item.sellerSku );
        return false;
    },
    select: function (event, ui) {
        console.log("select");
        setPriceByTimeValue(ui.item);
        return true;
    },
    change: function (e, ui) {
        console.log("change");
    }
});

$autocomplete.data( "ui-autocomplete" )._renderItem = function( ul, item ) {
    var $li = $('<li>'),
        $img = $('<img>');

    $img.attr({
      src: item.icon,
      style: "width:70px"
    });

    $li.attr('data-value', item.sellerSku);
    $li.append('<a href="#">');
    $li.find('a').append($img).append(item.value);

    return $li.appendTo(ul);
};

$autocomplete.on('keydown', function(e) {
    if (e.which == 13) {
        $('#btnsearch').trigger('click');
    }
});

//------------------------------------------------------------------------------
// Search prodcuts
//------------------------------------------------------------------------------
$("#btnsearch").click(function() {
    clearErrorLog();
    var searchKey = $searchInput.val();
    if (searchKey == '' || searchKey == null) {
        return;
    }
    var temp = searchKey.replace(/\ /g, "");
    if (temp == '' || temp == null) {
        return;
    }

    $.ajax({
        method: 'POST',
        url: endpoint.generateSearchPriceByTime(),
        async: false,
        contentType: "application/json",
        data: JSON.stringify({
            search_key: searchKey
        }),
        success: function(data) {
            console.log(data);
            fillAutocompleteSourceAndShowUp(data.data)
        },
        error: function(error) {
            console.log(error);
        }
    });
});

//------------------------------------------------------------------------------
// Additional functions
//------------------------------------------------------------------------------
function setPriceByTimeValue(autoCompleteItem) {
    $('input[name=txtSku]').val(autoCompleteItem.sellerSku);
    $('input[name=txtPrice01]').val(autoCompleteItem.specialPrice);
    $('input[name=txtPrice02]').val(autoCompleteItem.specialPrice);
    $('input[name=txtPrice03]').val(autoCompleteItem.specialPrice);
    $('input[name=txtSku]').focus();
    $searchInput.val("");
}

function fillAutocompleteSourceAndShowUp(products) {
    autocompleteSource = []
    $.each(products, function(key, value) {
        autocompleteSource.push({
            value: value['seller_sku'] + " - " + value['name'],
            icon: value['image'],
            sellerSku: value['seller_sku'],
            specialPrice: value['special_price'],
            name: value['name']
        })
    });
    $autocomplete.autocomplete({
        source: autocompleteSource
    });
    $autocomplete.data("uiAutocomplete").search($autocomplete.val());
}

function clearErrorLog() {
    $("#errorLog").html("");
}







