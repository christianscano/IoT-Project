$(document).ready(function() {
    function loadUsers(params) {
        $.ajax({
            url: '/api/v1/users',
            method: 'GET',
            success: function(response) {
                params.success(response.data.filter(user => user.username !== 'admin'));
            },
            error: function(response) {
                showToast(response.status, 'danger');
                params.error();
            }
        });
    }
    
    window.roleFormatter = function(value, row, index) {
        const roleMap = {
            'admin'   : 'System Manager',
            'security': 'Security Staff',
            'sysadmin': 'System Administrator',
        };
    
        return roleMap[value] || value;
    }
    
    $('#users-table').bootstrapTable({
        toggle        : "table",
        ajax          : loadUsers,
        pagination    : "true",
        pageSize      : "10",
        toolbar       : "#toolbar",
        search        : "true",
        visibleSearch : "true",
        ClickToSelect : "true",
        checkboxHeader: "false",
        escape        : "true"
    });

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
                    name    : $('#name').val(),
                    surname : $('#surname').val(),
                    username: $('#username').val(),
                    password: $('#password').val(),
                    role    : $('#role').val()
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
