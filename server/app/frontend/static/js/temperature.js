$(document).ready(function() {
    'use strict';

    var temperatureChart = null;

    function loadCurrentTemperature() {
        $.ajax({
            url: '/api/v1/temperature/status',
            success: function(response) {
                $('#current-temp').text(response.data.value + ' °C');
                $('#current-temp-time').text(response.data.timestamp);
            },
            error: function(response) {
                $('#current-temp').text(response.responseJSON.status);
            }
        });
    }

    function loadTemperatureTrend() {
        $.ajax({
            url: '/api/v1/temperature/trend',
            success: function(response) {
                var trendData = Array();
                var trendLabels = Array();

                response.data.forEach(function(item) {
                    trendData.push(item.value);
                    trendLabels.push(item.timestamp);
                });

                var ctx = document.getElementById('temperature-trend').getContext('2d');

                if (temperatureChart) {
                    temperatureChart.destroy();
                }

                temperatureChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: trendLabels,
                        datasets: [{
                            label: 'Temperature',
                            data: trendData,
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
                                },
                                beginAtZero: false,
                                suggestedMin: Math.min(...trendData) - 2.0,
                                suggestedMax: Math.max(...trendData) + 2.0
                            },
                        }
                    }
                });
            },
            error: function(response) {
                $('#temperature-trend').text(response.responseJSON.status);
            }
        });
    }

    clearAllIntervals();

    loadCurrentTemperature();
    loadTemperatureTrend();

    setInterval(loadCurrentTemperature, 10000);
    setInterval(loadTemperatureTrend, 100000);
});