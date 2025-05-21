document.addEventListener('DOMContentLoaded', function() {
    // Task Distribution Chart - Check if element exists first to prevent errors
    const taskDistributionCanvas = document.getElementById('taskDistributionChart');
    if (taskDistributionCanvas) {
        const data = {
            labels: ['Pending', 'In Progress', 'Completed', 'Overdue'],
            datasets: [{
                data: [
                    pending_count, 
                    in_progress_count, 
                    completed_count, 
                    overdue_count
                ],
                backgroundColor: getStatusColors(),
                borderWidth: 1
            }]
        };
        
        // Use the createDoughnutChart function from charts.js
        createDoughnutChart('taskDistributionChart', data, {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        });
    }
});
