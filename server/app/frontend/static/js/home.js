$(document).ready(function() {
    'use strict';
    
    window.timeoutList  = new Array();
    window.intervalList = new Array();

    window.oldSetTimeout    = window.setTimeout;
    window.oldSetInterval   = window.setInterval;
    window.oldClearTimeout  = window.clearTimeout;
    window.oldClearInterval = window.clearInterval;

    window.setTimeout = function(code, delay) {
        var retval = window.oldSetTimeout(code, delay);
        window.timeoutList.push(retval);
        return retval;
    };

    window.clearTimeout = function(id) {
        var ind = window.timeoutList.indexOf(id);
        if(ind >= 0) {
            window.timeoutList.splice(ind, 1);
        }
        var retval = window.oldClearTimeout(id);
        return retval;
    };
    
    window.setInterval = function(code, delay) {
        var retval = window.oldSetInterval(code, delay);
        window.intervalList.push(retval);
        return retval;
    };
    
    window.clearInterval = function(id) {
        var ind = window.intervalList.indexOf(id);
        if(ind >= 0) {
            window.intervalList.splice(ind, 1);
        }
        var retval = window.oldClearInterval(id);
        return retval;
    };
    
    window.clearAllTimeouts = function() {
        for(var i in window.timeoutList) {
            window.oldClearTimeout(window.timeoutList[i]);
        }
        window.timeoutList = new Array();
    };
    
    window.clearAllIntervals = function() {
        for(var i in window.intervalList) {
            window.oldClearInterval(window.intervalList[i]);
        }
        window.intervalList = new Array();
    };

    window.showToast = function (message, type) {
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

    $('#confirm-logout-btn').click(function(event) {
        event.preventDefault();

        $.ajax({
            url: '/api/v1/users/logout',
            success: function() {
                window.location.href = '/login';
            },
            error: function(response) {
                showToast(response.responseJSON.status, 'danger');
            }
        });
    });

    clearAllIntervals();
});