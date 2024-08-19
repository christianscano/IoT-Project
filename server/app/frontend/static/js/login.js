$(document).ready(function(){
    'use strict';
    
    $('#login-form').submit(function(event) {
        event.preventDefault();
        var form = $(this);

        if (form[0].checkValidity() === false) {
            event.stopPropagation();
            form.addClass('was-validated');
        } else {
            $.ajax({
                url: '/api/v1/users/signin',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    username: $('#username').val(),
                    password: $('#password').val()
                }),
                success: function() {
                    window.location.href = '/home';
                },
                error: function(response) {
                    $('#loginMessage').html(`<div class="alert alert-danger">${response.responseJSON.status}</div>`);
                }
            });
        }
    });
});