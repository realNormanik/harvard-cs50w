function initDashboardChart(labels, counts) {
    // Get the canvas element where the chart will be rendered
    const ctx = document.getElementById("stageChart");
    if (!ctx) return;

    new Chart(ctx, {
        // Display the data as a bar chart
        type: "bar",
        data: {
            // Labels displayed along the X-axis
            labels: labels,

            datasets: [{
                // Label used to describe the dataset
                label: "Number of deals in the stage",

                // Data values representing the number of deals for each stage
                data: counts,

                // Background color of the bars
                backgroundColor: "#3498db",

                // Rounds the corners of the bars
                borderRadius: 6
            }],
        },

        options: {
            // Make the chart responsive to the container size
            responsive: true,

            // Disable the default aspect ratio so the chart height
            // is determined by the CSS container
            maintainAspectRatio: false,
            plugins: {
                // Hide the legend because there is only one dataset
                legend: {
                    display: false
                },

                // Configure the chart title
                title: {
                    display: true,
                    text: "Deals in the Pipeline"
                },
            },

            scales: {
                y: {
                    // Start the Y-axis at zero
                    beginAtZero: true,

                    // Display whole numbers only on the Y-axis
                    ticks: {
                        precision: 0
                    },
                },
            },
        },
    });
};