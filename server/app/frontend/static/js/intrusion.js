$(document).ready(function() {
    'use strict';

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
            delay: 10000 
        });
        toastElement.show();
    }
    
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
                $('#system-status').text(response.status);
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
                $('#alarm-status').text(response.status);
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
                showToast(response.status, 'danger');
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
                showToast(response.status, 'danger');    
            }
        });
    });
    
    clearAllIntervals();
    updateIntrusionStatus();
    setInterval(updateIntrusionStatus, 2000);
});
