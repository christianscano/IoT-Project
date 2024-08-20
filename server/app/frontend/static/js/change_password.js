$(document).ready(function() {
    'use strict';
    
    $('#change-password-form').submit(function(event) {
        event.preventDefault();
        var form = $(this);

        if (form[0].checkValidity() === false) {
            event.stopPropagation();
            form.addClass('was-validated');
        } else {
            $.ajax({
                url: '/api/v1/users/change_password',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    'old_password'    : $('#current-password').val(),
                    'new_password'    : $('#new-password').val(),
                    'confirm_password': $('#confirm-password').val()
                }),
                success: function() {
                    $.ajax({
                        url: '/api/v1/users/logout',
                        success: function() {
                            window.location.href = '/login';
                        },
                        error: function(response) {
                            showToast(response.message, 'danger');
                        }
                    })
                },
                error: function(response) {
                    showToast(response.responseJSON.status, 'danger');
                    $('#change-password-form')[0].reset();
                }
            });
        }
    });

    clearAllIntervals();
});