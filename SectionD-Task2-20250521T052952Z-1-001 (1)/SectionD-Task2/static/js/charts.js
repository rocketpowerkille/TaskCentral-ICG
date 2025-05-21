/**
 * TasksCentral - Charts Configuration
 */

/**
 * Create a doughnut chart
 * @param {string} canvasId - ID of the canvas element
 * @param {object} data - Chart data object with labels and datasets
 * @param {object} options - Chart options (optional)
 * @returns {Chart} - Chart.js chart instance
 */
function createDoughnutChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Default options
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom'
            }
        }
    };
    
    // Merge default options with provided options
    const chartOptions = { ...defaultOptions, ...options };
    
    return new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: chartOptions
    });
}

/**
 * Create a bar chart
 * @param {string} canvasId - ID of the canvas element
 * @param {object} data - Chart data object with labels and datasets
 * @param {object} options - Chart options (optional)
 * @returns {Chart} - Chart.js chart instance
 */
function createBarChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Default options
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                position: 'top'
            }
        }
    };
    
    // Merge default options with provided options
    const chartOptions = { ...defaultOptions, ...options };
    
    return new Chart(ctx, {
        type: 'bar',
        data: data,
        options: chartOptions
    });
}

/**
 * Create a stacked bar chart
 * @param {string} canvasId - ID of the canvas element
 * @param {object} data - Chart data object with labels and datasets
 * @param {object} options - Chart options (optional)
 * @returns {Chart} - Chart.js chart instance
 */
function createStackedBarChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Default options
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                stacked: true,
            },
            y: {
                stacked: true,
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                position: 'top'
            }
        }
    };
    
    // Merge default options with provided options
    const chartOptions = { ...defaultOptions, ...options };
    
    return new Chart(ctx, {
        type: 'bar',
        data: data,
        options: chartOptions
    });
}

/**
 * Create a line chart
 * @param {string} canvasId - ID of the canvas element
 * @param {object} data - Chart data object with labels and datasets
 * @param {object} options - Chart options (optional)
 * @returns {Chart} - Chart.js chart instance
 */
function createLineChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Default options
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                position: 'top'
            }
        }
    };
    
    // Merge default options with provided options
    const chartOptions = { ...defaultOptions, ...options };
    
    return new Chart(ctx, {
        type: 'line',
        data: data,
        options: chartOptions
    });
}

/**
 * Create a pie chart
 * @param {string} canvasId - ID of the canvas element
 * @param {object} data - Chart data object with labels and datasets
 * @param {object} options - Chart options (optional)
 * @returns {Chart} - Chart.js chart instance
 */
function createPieChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Default options
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right'
            }
        }
    };
    
    // Merge default options with provided options
    const chartOptions = { ...defaultOptions, ...options };
    
    return new Chart(ctx, {
        type: 'pie',
        data: data,
        options: chartOptions
    });
}

/**
 * Update chart data
 * @param {Chart} chart - Chart.js chart instance
 * @param {object} newData - New data object
 */
function updateChartData(chart, newData) {
    chart.data = newData;
    chart.update();
}

/**
 * Get standard colors for task status charts
 * @returns {array} - Array of color codes
 */
function getStatusColors() {
    return [
        '#f39c12', // Pending - warning
        '#3498db', // In Progress - primary
        '#2ecc71', // Completed - success
        '#e74c3c'  // Overdue - danger
    ];
}

/**
 * Get standard colors for priority charts
 * @returns {array} - Array of color codes
 */
function getPriorityColors() {
    return [
        '#3498db', // Low - primary (blue)
        '#f39c12', // Medium - warning (orange)
        '#e74c3c', // High - danger (red)
        '#c0392b'  // Critical - dark red
    ];
}

/**
 * Get standard colors for category charts
 * @returns {array} - Array of color codes
 */
function getCategoryColors() {
    return [
        '#3498db', // Project - primary (blue)
        '#2ecc71', // BAU - success (green)
        '#9b59b6', // Meeting - purple
        '#e74c3c', // Incident - danger (red)
        '#34495e'  // Other - dark
    ];
}

/**
 * Create a progress chart (simple bar chart for completion rates)
 * @param {string} canvasId - ID of the canvas element
 * @param {array} labels - Labels for the chart (e.g., project names)
 * @param {array} values - Completion rate values
 * @returns {Chart} - Chart.js chart instance
 */
function createProgressChart(canvasId, labels, values) {
    const data = {
        labels: labels,
        datasets: [{
            label: 'Completion Rate',
            data: values,
            backgroundColor: '#2ecc71',
            borderWidth: 1
        }]
    };
    
    const options = {
        scales: {
            y: {
                beginAtZero: true,
                max: 100,
                title: {
                    display: true,
                    text: 'Completion Rate (%)'
                }
            }
        },
        plugins: {
            legend: {
                display: false
            }
        }
    };
    
    return createBarChart(canvasId, data, options);
}
