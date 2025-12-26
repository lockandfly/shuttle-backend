let shuttlesTable = null;

function formatDate(dateString) {
    if (!dateString) return "";
    if (dateString.includes("/")) return dateString;
    const d = new Date(dateString);
    if (isNaN(d)) return dateString;
    const day = String(d.getDate()).padStart(2, "0");
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const year = d.getFullYear();
    return `${day}/${month}/${year}`;
}

function formatTime(timeString) {
    if (!timeString) return "";
    if (/^\d{2}:\d{2}$/.test(timeString)) return timeString;
    const parts = timeString.split(":");
    if (parts.length !== 2) return timeString;
    const hh = String(parts[0]).padStart(2, "0");
    const mm = String(parts[1]).padStart(2, "0");
    return `${hh}:${mm}`;
}

function initTable() {
    shuttlesTable = $("#shuttlesTable").DataTable({
        columns: [
            { data: "Id", visible: false },
            {
                data: "Date",
                render: function (data) {
                    return formatDate(data);
                }
            },
            {
                data: "Time",
                render: function (data) {
                    return formatTime(data);
                }
            },
            { data: "Destination" },
            {
                data: null,
                orderable: false,
                render: function (row) {
                    return `
                        <button class="btn btn-sm btn-outline-light me-1" data-action="edit">
                            <i class="bi bi-pencil"></i> Modifica
                        </button>
                        <button class="btn btn-sm btn-outline-danger" data-action="delete">
                            <i class="bi bi-trash"></i> Elimina
                        </button>
                    `;
                }
            }
        ],
        order: [[1, "asc"], [2, "asc"]],
        pageLength: 10,
        language: { url: "https://cdn.datatables.net/plug-ins/1.13.8/i18n/it-IT.json" }
    });

    $("#shuttlesTable tbody").on("click", "button", async function () {
        const action = this.dataset.action;
        const row = shuttlesTable.row($(this).parents("tr")).data();
        if (action === "edit") openShuttleModal(row);
        if (action === "delete") handleDeleteShuttle(row);
    });
}

async function loadShuttles() {
    const date = document.getElementById("filterDate").value;
    try {
        const data = await fetchShuttles(date || null);
        shuttlesTable.clear();
        shuttlesTable.rows.add(data);
        shuttlesTable.draw();
        const lastUpdateEl = document.getElementById("lastUpdate");
        if (lastUpdateEl) lastUpdateEl.textContent = `Aggiornato: ${new Date().toLocaleTimeString()}`;
    } catch (err) {
        showToast(err.message || "Errore nel caricamento delle navette.", "error");
    }
}

async function handleDeleteShuttle(shuttle) {
    const msg = `Eliminare la navetta del ${formatDate(shuttle.Date)} alle ${formatTime(shuttle.Time)}?`;
    if (!confirm(msg)) return;
    try {
        await deleteShuttleById(shuttle.Id);
        showToast("Navetta eliminata.");
        await loadShuttles();
        await refreshCharts();
    } catch (err) {
        showToast(err.message || "Errore durante l'eliminazione.", "error");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    initTable();
    loadShuttles();
    document.getElementById("btnFilter").addEventListener("click", loadShuttles);
    document.getElementById("btnClearFilter").addEventListener("click", () => {
        document.getElementById("filterDate").value = "";
        loadShuttles();
    });
});

window.loadShuttles = loadShuttles;
window.formatDate = formatDate;
window.formatTime = formatTime;
