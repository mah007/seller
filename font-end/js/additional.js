//------------------------------------------------------------------------------
// Logout
//------------------------------------------------------------------------------
$('#logoutButton').click(function() {
  cookie.clearToken('token');
  cookie.clearToken('myUser');
  cookie.clearToken('username');
  window.location.href = "../login";
});

//-------------------------------------------------------------------------------------
// Internal plugins
//-------------------------------------------------------------------------------------
var Additional = function() {
}

//-------------------------------------------------------------------------------------
// Input money
//-------------------------------------------------------------------------------------
Additional.prototype.initMoneyInput = function() {
    $('.table').find('input.input-money').click(function () {
       $(this).select();
    });
    // Money format with comma
    $('.table').find('input.input-money').keyup(function(event) {
        if(event.which >= 37 && event.which <= 40) return;

        $(this).val(function(index, value) {
            return value
            .replace(/\D/g, "")
            .replace(/\B(?=(\d{3})+(?!\d))/g, ",")
            ;
        });
    });
    // Number only, but accept comma and decimal
    $('.table').find('input.input-money').on("keypress",function(e){
        switch (e.key) {
            case "1":
            case "2":
            case "3":
            case "4":
            case "5":
            case "6":
            case "7":
            case "8":
            case "9":
            case "0":
            case "Backspace":
            return true;

            case ".": {
                if ($(this).val().indexOf(".") == -1) return true;
                else return false;
            }

            case ",": {
                if ($(this).val().indexOf(",") == -1) return true;
                else return false;
            }

            default: {
                return false;
            }
        }
    });
}







