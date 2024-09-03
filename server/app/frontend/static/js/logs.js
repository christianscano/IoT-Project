$(document).ready(function () {
    function loadLogs(params) {
        $.ajax({
            url: '/api/v1/logs',
            data: params.data,
            success: function (response) {
                params.success(response.data);
            },
            error: function (response) {
                showToast(response.responseJSON.status, 'danger');
                params.error();
            }
        });
    };

    function queryParams(params) {
        if ($('#startDate').val() !== '') {
            params['start_date'] = $('#startDate').val();
        }

        if ($('#endDate').val() !== '') {
            params['end_date'] = $('#endDate').val();
        }

        if ($('#username').val() !== '') {
            params.username = $('#username').val();
        }

        return params;
    }

    $('#logs-table').bootstrapTable({
        toggle         : "table",
        ajax           : loadLogs,
        queryParams    : queryParams,
        pagination     : "true",
        pageSize       : "10",
        toolbar        : "#toolbar",
        escape         : "true",
    });

    $('#startDate').datepicker({
        format        : 'yyyy-mm-dd',
        autoclose     : true,
        todayHighlight: true,
	orientation   : 'auto bottom',
        templates: {
            leftArrow : '<i class="fa fa-chevron-left"></i>',
            rightArrow: '<i class="fa fa-chevron-right"></i>'
        }
    });

    $('#endDate').datepicker({
        format        : 'yyyy-mm-dd',
        autoclose     : true,
        todayHighlight: true,
	orientation   : 'auto bottom',
        templates: {
            leftArrow : '<i class="fa fa-chevron-left"></i>',
            rightArrow: '<i class="fa fa-chevron-right"></i>'
        }
    });

    $('#filterButton').click(function () {
        $('#logs-table').bootstrapTable('refresh');
    });

    clearAllIntervals();
});
