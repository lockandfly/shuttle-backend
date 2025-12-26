let shuttlesTable = null;

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
                searchable: false,
                render: function (data, type, row) {
                    return `
                        <button class="btn btn-sm btn-outline-light me-1" data-action="edit">Modifica</button>
                        <button class="btn btn-sm btn-outline-danger" data-action="delete">Elimina</button>
                    `;
                }
            }
        ],
        order: [[1, "asc"], [2, "asc"]],
        paging: true,
        pageLength: 10,
        lengthChange: false,
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.13.8/i18n/it-IT.json"
        }
    });

    // Azioni edit/delete
    $("#shuttlesTable tbody").on("click", "button", async function () {
        const action = this.getAttribute("data-action");
        const data = shuttlesTable.row($(this).parents("tr")).data();

        if (action === "edit") {
            openShuttleModal(data);
        } else if (action === "delete") {
            await handleDeleteShuttle(data);
        }
    });

    // Filtri
    document.getElementById("btnFilter").addEventListener("click", () => loadShuttles());
    document.getElementById("btnClearFilter").addEventListener("click", async () => {
        document.getElementById("filterDate").value = "";
        await loadShuttles();
    });
}

async function loadShuttles() {
    const dateFilter = document.getElementById("filterDate").value.trim();

    try {
        const shuttles = await fetchShuttles(dateFilter || null);
        shuttlesTable.clear();
        shuttlesTable.rows.add(shuttles);
        shuttlesTable.draw();

        const now = new Date();
        document.getElementById("lastUpdate").textContent =
            `Aggiornato alle ${now.toLocaleTimeString()} (${shuttles.length} record)`;
    } catch (err) {
        console.error(err);
        showToast("Errore nel caricamento navette.", "error");
    }
}

async function handleDeleteShuttle(shuttle) {
    if (!confirm(`Vuoi davvero eliminare la navetta per "${shuttle.Destination}" del ${shuttle.Date} alle ${shuttle.Time}?`)) {
        return;
    }

    try {
        const res = await deleteShuttleById(shuttle.Id);
        if (res.error) {
            showToast(res.error, "error");
            return;
        }

        showToast("Navetta eliminata.", "success");
        await loadShuttles();
        await refreshCharts();
    } catch (err) {
        console.error(err);
        showToast("Errore nella cancellazione.", "error");
    }
}
