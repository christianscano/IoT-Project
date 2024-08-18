$(document).ready(function() {
    function load_current_temperature() {
        $.ajax({
            url: '/api/v1/temperature/status',
            method: 'GET',
            success: function(response) {
                $('#current-temp').text(response.value + ' °C');
                $('#current-temp-time').text(response.timestamp);
            },
            error: function() {
                $('#current-temp').text('Error loading temperature');
            }
        });
    }

    function load_temperature_trend() {
        $.ajax({
            url: '/api/v1/temperature/trend',
            method: 'GET',
            success: function(response) {
                var trendData = response.values;

                var ctx = document.getElementById('temperature-trend').getContext('2d');
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: time_data,
                        datasets: [{
                            label: 'Temperature',
                            data: trend_data,
                            backgroundColor: 'transparent',
                            fill: false,
                            borderColor: '#007bff',
                            borderWidth: 2,
                            pointBackgroundColor: '#007bff'
                        }]
                    },
                    options: {
                        layout: {
                            padding: {
                                left: 80,
                                right: 80,
                                top: 20,
                                bottom: 20
                            }
                        },
                        plugins: {
                            legend: {
                                display: false
                            },
                        },
                        scales: {
                            x: {
                                display: true,
                                ticks: {
                                    maxTicksLimit: 10,
                                    padding: 10
                                }
                            },
                            y: {
                                display: true,
                                title: {
                                    display: true,
                                    text: 'Temperature (°C)'
                                },
                                ticks: {
                                    maxTicksLimit: 15,
                                }
                            },
                        }
                    }
                });
            },
            error: function() {
                $('#temperature-trend').text('Error loading trend data');
            }
        });
    }

    // Load initial temperature data
    load_current_temperature();
    load_temperature_trend();

    // Auto-refresh temperature data every 10 seconds
    setInterval(load_current_temperature, 10000);
    setInterval(load_temperature_trend, 100000);
});