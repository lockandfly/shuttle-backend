let chartByDay = null;
let chartByDestination = null;

document.addEventListener("DOMContentLoaded", () => {
    initCharts();
});

function initCharts() {
    chartByDay = new Chart(document.getElementById("chartByDay"), {
        type: "bar",
        data: { labels: [], datasets: [{ label: "Navette", data: [], backgroundColor: "rgba(54,162,235,0.7)" }] },
        options: { scales: { x: { ticks: { color: "#fff" } }, y: { ticks: { color: "#fff" }, beginAtZero: true } } }
    });

    chartByDestination = new Chart(document.getElementById("chartByDestination"), {
        type: "pie",
        data: { labels: [], datasets: [{ data: [], backgroundColor: ["#0d6efd","#6610f2","#6f42c1","#d63384","#dc3545","#fd7e14","#ffc107","#198754","#20c997","#0dcaf0"] }] },
        options: { plugins: { legend: { labels: { color: "#fff" } } } }
    });

    refreshCharts();
}

async function refreshCharts() {
    const data = await fetchShuttles();

    const byDay = {};
    const byDest = {};

    data.forEach(s => {
        byDay[s.Date] = (byDay[s.Date] || 0) + 1;
        byDest[s.Destination] = (byDest[s.Destination] || 0) + 1;
    });

    chartByDay.data.labels = Object.keys(byDay);
    chartByDay.data.datasets[0].data = Object.values(byDay);
    chartByDay.update();

    chartByDestination.data.labels = Object.keys(byDest);
    chartByDestination.data.datasets[0].data = Object.values(byDest);
    chartByDestination.update();
}
