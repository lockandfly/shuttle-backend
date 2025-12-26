let shuttlesTable = null;

document.addEventListener("DOMContentLoaded", () => {
    initTable();
    loadShuttles();

    document.getElementById("btnFilter").addEventListener("click", loadShuttles);
    document.getElementById("btnClearFilter").addEventListener("click", () => {
        document.getElementById("filterDate").value = "";
        loadShuttles();
    });
});

function formatDate(dateString) {
    if (!dateString) return "";

    // Se è già nel formato gg/mm/aaaa
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

    // Se è già nel formato HH:MM
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
                data: null,
                render: function (row) {
                    const t = row.Time || row.time || row.Ora || row.ora;
                    return formatTime(t);
                }
            },

            { data: "Destination" },

            {
                data: null,
                orderable: false,
                render: () => `
                    <button class="btn btn-sm btn-outline-light me-1" data-action="edit">
                        <i class="bi bi-pencil"></i> Modifica
                    </button>
                    <button class="btn btn-sm btn-outline-danger" data-action="delete">
                        <i class="bi bi-trash"></i> Elimina
                    </button>
                `
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
        if (lastUpdateEl) {
            lastUpdateEl.textContent =
                `Aggiornato: ${new Date().toLocaleTimeString()}`;
        }
    } catch (err) {
        showToast(err.message || "Errore nel caricamento delle navette.", "error");
    }
}

async function handleDeleteShuttle(shuttle) {
    const msg = `Eliminare la navetta del ${formatDate(shuttle.Date)} alle ${formatTime(shuttle.Time)}?`;
    if (!confirm(msg)) return;

    try {
        const res = await deleteShuttleById(shuttle.Id);
        if (res.error) {
            showToast(res.error, "error");
            return;
        }

        showToast("Navetta eliminata.");
        await loadShuttles();
        await refreshCharts();
    } catch (err) {
        showToast(err.message || "Errore durante l'eliminazione.", "error");
    }
}

// Espongo alcune funzioni globalmente se servono altrove
window.loadShuttles = loadShuttles;
window.formatDate = formatDate;
window.formatTime = formatTime;
