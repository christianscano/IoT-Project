$(document).ready(function() {
    'use strict';
    
    function updateIntrusionStatus() {
        $.ajax({
            url: '/api/v1/intrusion/status',
            success: function(response) {
                var systemStatus = response.enabled;
               
                if (systemStatus) {
                    $('#system-status').text("Active");
                    $('#system-button').text("Disable");
                    $('#alarm-card').removeClass('d-none');
                    updateAlarmStatus();
                } else {
                    $('#system-status').text("Disabled");
                    $('#system-button').text("Enable");
                    $('#alarm-card').addClass('d-none');
                }
            },
            error: function(response) {
                $("#alarm-card").addClass('d-none');
                $('#system-status').text(response.responseJSON.status);
            }
        });
    }

    function updateAlarmStatus() {
        $.ajax({
            url: '/api/v1/intrusion/status_alarm',
            success: function(response) {
                var alarmStatus = response.enabled;

                if (alarmStatus) {
                    $('#alarm-status').text("Actived");
                    $('#alarm-button').removeAttr('disabled');
                } else {
                    $('#alarm-status').text("Disabled");
                    $('#alarm-button').attr('disabled', 'disabled');
                }
            },
            error: function(response) {
                $('#alarm-status').text(response.responseJSON.status);
            }
        });
    }

    $('#system-button').click(function() {
        var action = $('#system-status').text() === 'Active' ? 'disable' : 'enable';
        var apiUrl = '/api/v1/intrusion/' + action;

        $.ajax({
            url: apiUrl,
            success: function(response) {
                showToast(response.status, 'success');
                updateIntrusionStatus(); 
            },
            error: function(response) {
                showToast(response.responseJSON.status, 'danger');
            }
        });
    });

    $('#alarm-button').click(function() {
        $.ajax({
            url: '/api/v1/intrusion/disable_alarm',
            success: function(response) {
                showToast(response.status, 'success');
                updateAlarmStatus();
            },
            error: function(response) {
                showToast(response.responseJSON.status, 'danger');    
            }
        });
    });
    
    clearAllIntervals();
    updateIntrusionStatus();
    setInterval(updateIntrusionStatus, 2000);
});
