$(document).ready(function() {
    function loadUsers(params) {
        $.ajax({
            url: '/api/v1/users',
            success: function(response) {
                params.success(response.data.filter(user => user.role !== 'admin' && user.tag_id !== null));
            },
            error: function(response) {
                showToast(response.status, 'danger');
                params.error();
            }
        });
    }
        
    $('#tags-table').bootstrapTable({
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

    $('#tags-table').on('check.bs.table uncheck.bs.table check-all.bs.table uncheck-all.bs.table', function() {
        var selections = $('#tags-table').bootstrapTable('getSelections');
        $('#delete-tag-btn').prop('disabled', selections.length === 0);
    });

    $('#confirm-delete-btn').click(function() {
        var selections = $('#tags-table').bootstrapTable('getSelections');
        var users = selections.map(user => user.username);

        var requestsCompleted = 0;

        function handleCompletion(msg, isSuccess) {
            requestsCompleted++;
            if (isSuccess) {
                showToast(msg, 'success');
            } else {
                showToast(msg, 'danger');
            }

            if (requestsCompleted === users.length) {
                $('#deleteTagModal').modal('hide');
                $('#tags-table').bootstrapTable('refresh');
            }
        }

        users.forEach(function(user) {
            $.ajax({
                url: '/api/v1/users/remove_tag',
                type: 'POST',
                data: JSON.stringify({ username: user }),
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

    $('#add-tag-form').submit(function(event) {
        event.preventDefault();
        var form = $(this);

        if (form[0].checkValidity() === false) {
            event.stopPropagation();
            form.addClass('was-validated');
        } else {
            $.ajax({
                url: '/api/v1/users/add_tag',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    username: $('#username').val(),
                    tag_id  : $('#tag-id').val()
                }),
                success: function(response) {
                    showToast(response.status, 'success');
                    $('#addTagModal').modal('hide');
                    $('#tags-table').bootstrapTable('refresh');
                    form[0].reset();
                    form.removeClass('was-validated');
                },
                error: function(response) {
                    showToast(response.status, 'danger');
                }
            });
        }
    });

    $('#addTagModal').on('shown.bs.modal', function () {
        var $dropdown = $('#username');
        
        $dropdown.empty();        
        $dropdown.append('<option value="" disabled selected>Select an user</option>');

        $.ajax({
            url: '/api/v1/users',
            success: function(response) {
                $.each(response.data, function(index, user) {
                    if (user.role !== 'admin' && user.tag_id === null) {
                        $dropdown.append(
                            $('<option></option>').val(user.username).text(user.username)
                        );
                    }
                });
            },
            error: function(response) {
                showToast(response.status, 'danger');
            }
        });
    });

    clearAllIntervals();
});
