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

function initTable() {
    shuttlesTable = $("#shuttlesTable").DataTable({
        columns: [
            { data: "Id", visible: false },
            { data: "Date" },
            { data: "Time" },
            { data: "Destination" },
            {
                data: null,
                orderable: false,
                render: () => `
                    <button class="btn btn-sm btn-outline-light me-1" data-action="edit">Modifica</button>
                    <button class="btn btn-sm btn-outline-danger" data-action="delete">Elimina</button>
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
    const data = await fetchShuttles(date || null);

    shuttlesTable.clear();
    shuttlesTable.rows.add(data);
    shuttlesTable.draw();

    document.getElementById("lastUpdate").textContent =
        `Aggiornato: ${new Date().toLocaleTimeString()}`;
}

async function handleDeleteShuttle(shuttle) {
    if (!confirm(`Eliminare la navetta del ${shuttle.Date} alle ${shuttle.Time}?`)) return;

    const res = await deleteShuttleById(shuttle.Id);
    if (res.error) return showToast(res.error, "error");

    showToast("Navetta eliminata.");
    loadShuttles();
    refreshCharts();
}
