$(document).ready(function(){
    'use strict';
    
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = $('.needs-validation');
    
    // Loop over them and prevent submission
    forms.each(function() {
        $(this).on('submit', function(event) {
        if (!this.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
    
        $(this).addClass('was-validated');
        });
    });

    $('#login-form').on('submit', function(event) {
        event.preventDefault();

        const username = $('#username').val();
        const password = $('#password').val();

        $.ajax({
            url: '/api/v1/users/signin',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                username: username,
                password: password
            }),
            success: function(response) {
                window.location.href = '/home';
            },
            error: function(response) {
                $('#loginMessage').html(`<div class="alert alert-danger">${response.responseJSON.status}</div>`);
            }
        });
    });
});


