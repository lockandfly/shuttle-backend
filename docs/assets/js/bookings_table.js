let bookingsTable = null;

function formatBookingDate(dateString) {
    if (!dateString) return "";
    if (dateString.includes("/")) return dateString;
    const d = new Date(dateString);
    if (isNaN(d)) return dateString;
    const day = String(d.getDate()).padStart(2, "0");
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const year = d.getFullYear();
    return `${day}/${month}/${year}`;
}

function formatBookingTime(timeString) {
    if (!timeString) return "";
    if (/^\d{2}:\d{2}$/.test(timeString)) return timeString;
    const parts = timeString.split(":");
    if (parts.length < 2) return timeString;
    const hh = String(parts[0]).padStart(2, "0");
    const mm = String(parts[1]).padStart(2, "0");
    return `${hh}:${mm}`;
}

function initBookingsTable() {
    bookingsTable = $("#bookingsTable").DataTable({
        columns: [
            { data: "Id", visible: false },
            { data: "CustomerName" },
            { data: "Phone" },
            { data: "Plate" },
            {
                data: null,
                render: function (row) {
                    const d = formatBookingDate(row.ArrivalDate);
                    const t = formatBookingTime(row.ArrivalTime);
                    return `${d} ${t}`;
                }
            },
            {
                data: null,
                render: function (row) {
                    const d = formatBookingDate(row.ReturnDate);
                    const t = formatBookingTime(row.ReturnTime);
                    return `${d} ${t}`;
                }
            },
            { data: "People" },
            { data: "ServiceType" },
            {
                data: null,
                orderable: false,
                render: function () {
                    return `
                        <button class="btn btn-sm btn-outline-light me-1" data-action="edit">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" data-action="delete">
                            <i class="bi bi-trash"></i>
                        </button>
                    `;
                }
            }
        ],
        order: [[4, "asc"]],
        pageLength: 10,
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.13.8/i18n/it-IT.json"
        }
    });

    $("#bookingsTable tbody").on("click", "button", async function () {
        const action = this.dataset.action;
        const row = bookingsTable.row($(this).parents("tr")).data();
        if (action === "edit") openBookingModal(row);
        if (action === "delete") handleDeleteBooking(row);
    });
}

async function loadBookings() {
    const date = document.getElementById("filterDate").value;
    try {
        const data = await fetchBookings(date || null);
        bookingsTable.clear();
        bookingsTable.rows.add(data);
        bookingsTable.draw();
        const lastUpdateEl = document.getElementById("lastUpdate");
        if (lastUpdateEl) lastUpdateEl.textContent = `Aggiornato: ${new Date().toLocaleTimeString()}`;
    } catch (err) {
        showBookingToast(err.message || "Errore nel caricamento delle prenotazioni.", "error");
    }
}

async function handleDeleteBooking(booking) {
    const msg = `Eliminare la prenotazione di ${booking.CustomerName} del ${formatBookingDate(booking.ArrivalDate)}?`;
    if (!confirm(msg)) return;
    try {
        await deleteBookingById(booking.Id);
        showBookingToast("Prenotazione eliminata.");
        await loadBookings();
    } catch (err) {
        showBookingToast(err.message || "Errore durante l'eliminazione.", "error");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    initBookingsTable();
    loadBookings();
    document.getElementById("btnFilter").addEventListener("click", loadBookings);
    document.getElementById("btnClearFilter").addEventListener("click", () => {
        document.getElementById("filterDate").value = "";
        loadBookings();
    });
});

window.loadBookings = loadBookings;
