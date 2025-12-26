let shuttlesPerDayChart = null;
let shuttlesPerDestinationChart = null;

function initCharts() {
    const ctxDay = document.getElementById("shuttlesPerDayChart");
    const ctxDest = document.getElementById("shuttlesPerDestinationChart");

    if (ctxDay) {
        shuttlesPerDayChart = new Chart(ctxDay, {
            type: "bar",
            data: {
                labels: [],
                datasets: [{
                    label: "Navette per giorno",
                    data: [],
                    backgroundColor: "rgba(54,162,235,0.7)",
                    borderColor: "rgba(54,162,235,1)",
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: { duration: 300 },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                },
                plugins: { legend: { display: false } }
            }
        });
    }

    if (ctxDest) {
        shuttlesPerDestinationChart = new Chart(ctxDest, {
            type: "bar",
            data: {
                labels: [],
                datasets: [{
                    label: "Navette per destinazione",
                    data: [],
                    backgroundColor: [
                        "#00b894","#0984e3","#fdcb6e",
                        "#d63031","#6c5ce7","#e17055"
                    ],
                    borderWidth: 0,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: { duration: 300 },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                },
                plugins: { legend: { display: false } }
            }
        });
    }
}

async function refreshCharts() {
    try {
        const shuttles = await fetchShuttles(null);

        const byDay = {};
        shuttles.forEach(s => {
            const d = s.Date || "";
            if (!d) return;
            byDay[d] = (byDay[d] || 0) + 1;
        });

        const dayLabels = Object.keys(byDay).sort((a, b) => {
            const [da, ma, ya] = a.split("/");
            const [db, mb, yb] = b.split("/");
            return new Date(`${ya}-${ma}-${da}`) - new Date(`${yb}-${mb}-${db}`);
        });

        const dayValues = dayLabels.map(d => byDay[d]);

        if (shuttlesPerDayChart) {
            shuttlesPerDayChart.data.labels = dayLabels;
            shuttlesPerDayChart.data.datasets[0].data = dayValues;
            shuttlesPerDayChart.update();
        }

        const byDest = {};
        shuttles.forEach(s => {
            const dest = (s.Destination || "").trim();
            if (!dest) return;
            byDest[dest] = (byDest[dest] || 0) + 1;
        });

        const destLabels = Object.keys(byDest);
        const destValues = destLabels.map(d => byDest[d]);

        if (shuttlesPerDestinationChart) {
            shuttlesPerDestinationChart.data.labels = destLabels;
            shuttlesPerDestinationChart.data.datasets[0].data = destValues;
            shuttlesPerDestinationChart.update();
        }

    } catch (err) {
        if (typeof showToast === "function")
            showToast(err.message || "Errore nel caricamento dei grafici.", "error");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    initCharts();
    refreshCharts();
});

window.refreshCharts = refreshCharts;
