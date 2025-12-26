let chartByDay = null;
let chartByDestination = null;

function initCharts() {
    const ctxDay = document.getElementById("chartByDay").getContext("2d");
    const ctxDest = document.getElementById("chartByDestination").getContext("2d");

    chartByDay = new Chart(ctxDay, {
        type: "bar",
        data: {
            labels: [],
            datasets: [
                {
                    label: "Navette",
                    data: [],
                    backgroundColor: "rgba(54, 162, 235, 0.7)"
                }
            ]
        },
        options: {
            scales: {
                x: { ticks: { color: "#fff" } },
                y: { ticks: { color: "#fff" }, beginAtZero: true }
            },
            plugins: {
                legend: { labels: { color: "#fff" } }
            }
        }
    });

    chartByDestination = new Chart(ctxDest, {
        type: "pie",
        data: {
            labels: [],
            datasets: [
                {
                    label: "Navette",
                    data: [],
                    backgroundColor: [
                        "#0d6efd",
                        "#6610f2",
                        "#6f42c1",
                        "#d63384",
                        "#dc3545",
                        "#fd7e14",
                        "#ffc107",
                        "#198754",
                        "#20c997",
                        "#0dcaf0"
                    ]
                }
            ]
        },
        options: {
            plugins: {
                legend: { labels: { color: "#fff" } }
            }
        }
    });

    refreshCharts();
}

async function refreshCharts() {
    try {
        const allShuttles = await fetchShuttles(null);

        // Aggrega per giorno
        const byDay = {};
        const byDest = {};

        for (const s of allShuttles) {
            byDay[s.Date] = (byDay[s.Date] || 0) + 1;
            byDest[s.Destination] = (byDest[s.Destination] || 0) + 1;
        }

        const dayLabels = Object.keys(byDay).sort();
        const dayValues = dayLabels.map(d => byDay[d]);

        chartByDay.data.labels = dayLabels;
        chartByDay.data.datasets[0].data = dayValues;
        chartByDay.update();

        const destLabels = Object.keys(byDest);
        const destValues = destLabels.map(d => byDest[d]);

        chartByDestination.data.labels = destLabels;
        chartByDestination.data.datasets[0].data = destValues;
        chartByDestination.update();
    } catch (err) {
        console.error(err);
        showToast("Errore nel caricamento grafici.", "error");
    }
}
