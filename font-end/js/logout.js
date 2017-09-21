//-------------------------------------------------------------------------------------
// Logout
//-------------------------------------------------------------------------------------
$('#logoutButton').click(function() {
    cookie.clearToken('token');
    cookie.clearToken('myUser');
    cookie.clearToken('username');
    window.location.href = "../login";
});