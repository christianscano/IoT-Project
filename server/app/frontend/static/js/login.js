$(document).ready(function(){
    $('#loginButton').click(function(){
        const username = $('#username').val();
        const password = $('#password').val();

        $.ajax({
            url: '/api/v1/user/login',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                username: username,
                password: password
            }),
            success: function(response) {
                window.location.href = '/dashboard';
            },
            error: function(response) {
                $('#loginMessage').html(`<div class="alert alert-danger">${response.responseJSON.status}</div>`);
            }
        });
    });
});
