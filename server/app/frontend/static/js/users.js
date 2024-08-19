function loadUsers(params) {
    $.ajax({
        url: '/api/v1/users',
        method: 'GET',
        success: function(response) {
            console.log(response.data);
            params.success(response.data.filter(user => user.username !== 'admin'));
        },
        error: function(response) {
            console.log(response.status);
            showToast(response.status, 'danger');
            params.error();
        }
    });
}

function roleFormatter(value, row, index) {
    const roleMap = {
        'admin'   : 'System Manager',
        'security': 'Security Staff',
        'sysadmin': 'System Administrator',
    };

    return roleMap[value] || value;
}

function customLoading() {
    return '<i class="fa fa-spinner fa-spin fa-fw fa-2x"></i>'
}

$(document).ready(function() {
    function showToast(message, type) {
        var toastId = 'toast-' + Date.now();
        var iconHTML = '';

        if (type === 'success') {
            iconHTML = '<i class="bi bi-check-circle-fill me-2"></i>';
        } else if (type === 'danger') {
            iconHTML = '<i class="bi bi-exclamation-triangle-fill me-2"></i>';
        }

        var toastHTML = `
            <div id="${toastId}" class="toast align-items-center text-bg-${type} border-0 mb-2" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        ${iconHTML}${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>`;

        $('#toast-container').append(toastHTML);

        var toastElement = new bootstrap.Toast(document.getElementById(toastId), {
            delay: 3000
        });
        toastElement.show();
    }

    // Abilita/Disabilita il pulsante di eliminazione in base alla selezione
    $('#users-table').on('check.bs.table uncheck.bs.table check-all.bs.table uncheck-all.bs.table', function() {
        var selections = $('#users-table').bootstrapTable('getSelections');
        $('#delete-user-btn').prop('disabled', selections.length === 0);
    });

    $('#confirm-delete-btn').click(function() {
        var selections = $('#users-table').bootstrapTable('getSelections');
        var ids = selections.map(user => user.id);

        var requestsCompleted = 0;

        function handleCompletion(msg, isSuccess) {
            requestsCompleted++;
            if (isSuccess) {
                showToast(msg, 'success');
            } else {
                showToast(msg, 'danger');
            }

            if (requestsCompleted === ids.length) {
                $('#deleteUserModal').modal('hide');
                $('#users-table').bootstrapTable('refresh');
            }
        }

        ids.forEach(function(id) {
            $.ajax({
                url: '/api/v1/users/' + id,
                type: 'DELETE',
                contentType: 'application/json',
                success: function(response) {
                    handleCompletion(response.status, true);
                },
                error: function(response) {
                    handleCompletion(response.status, false);
                }
            });
        });
    });

    $('#add-user-form').submit(function(event) {
        event.preventDefault();
        var form = $(this);

        if (form[0].checkValidity() === false) {
            event.stopPropagation();
            form.addClass('was-validated');
        } else {
            $.ajax({
                url: '/api/v1/users',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    name: $('#name').val(),
                    surname: $('#surname').val(),
                    username: $('#username').val(),
                    password: $('#password').val(),
                    role: $('#role').val()
                }),
                success: function(response) {
                    showToast(response.status, 'success');
                    $('#addUserModal').modal('hide');
                    $('#users-table').bootstrapTable('refresh');
                    form[0].reset();
                    form.removeClass('was-validated');
                },
                error: function(response) {
                    showToast(response.status, 'danger');
                }
            });
        }
    });

    clearAllIntervals();
});
