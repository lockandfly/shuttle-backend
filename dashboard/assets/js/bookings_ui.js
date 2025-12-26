let bookingModal = null;
let editingBookingId = null;

function showBookingToast(message, type = "success") {
    const containerId = "toast-container";
    let container = document.getElementById(containerId);
    if (!container) {
        container = document.createElement("div");
        container.id = containerId;
        container.style.position = "fixed";
        container.style.top = "1rem";
        container.style.right = "1rem";
        container.style.zIndex = "9999";
        document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = "toast align-items-center text-bg-" + (type === "error" ? "danger" : "success");
    toast.role = "alert";
    toast.ariaLive = "assertive";
    toast.ariaAtomic = "true";
    toast.style.minWidth = "220px";
    toast.style.marginBottom = "0.5rem";

    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    container.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
    bsToast.show();
    toast.addEventListener("hidden.bs.toast", () => toast.remove());
}

function openBookingModal(booking = null) {
    const modalEl = document.getElementById("bookingModal");
    if (!bookingModal) {
        bookingModal = new bootstrap.Modal(modalEl);
    }

    const titleEl = modalEl.querySelector(".modal-title");

    const f = (id) => document.getElementById(id);

    if (booking) {
        editingBookingId = booking.Id;
        titleEl.textContent = "Modifica prenotazione";

        f("bkCustomerName").value = booking.CustomerName || "";
        f("bkPhone").value = booking.Phone || "";
        f("bkEmail").value = booking.Email || "";
        f("bkPlate").value = booking.Plate || "";
        f("bkArrivalDate").value = booking.ArrivalDate || "";
        f("bkArrivalTime").value = booking.ArrivalTime || "";
        f("bkReturnDate").value = booking.ReturnDate || "";
        f("bkReturnTime").value = booking.ReturnTime || "";
        f("bkPeople").value = booking.People || "";
        f("bkServiceType").value = booking.ServiceType || "";
        f("bkShuttleId").value = booking.ShuttleId || "";
        f("bkNotes").value = booking.Notes || "";
    } else {
        editingBookingId = null;
        titleEl.textContent = "Nuova prenotazione";

        f("bkCustomerName").value = "";
        f("bkPhone").value = "";
        f("bkEmail").value = "";
        f("bkPlate").value = "";
        f("bkArrivalDate").value = "";
        f("bkArrivalTime").value = "";
        f("bkReturnDate").value = "";
        f("bkReturnTime").value = "";
        f("bkPeople").value = "";
        f("bkServiceType").value = "";
        f("bkShuttleId").value = "";
        f("bkNotes").value = "";
    }

    bookingModal.show();
}

async function handleBookingFormSubmit(event) {
    event.preventDefault();

    const f = (id) => document.getElementById(id).value.trim();

    const payload = {
        customer_name: f("bkCustomerName"),
        phone: f("bkPhone") || null,
        email: f("bkEmail") || null,
        plate: f("bkPlate") || null,
        arrival_date: f("bkArrivalDate"),
        arrival_time: f("bkArrivalTime"),
        return_date: f("bkReturnDate"),
        return_time: f("bkReturnTime"),
        people: f("bkPeople") || null,
        service_type: f("bkServiceType") || null,
        shuttle_id: f("bkShuttleId") || null,
        notes: f("bkNotes") || null
    };

    if (!payload.customer_name || !payload.arrival_date || !payload.arrival_time || !payload.return_date || !payload.return_time) {
        showBookingToast("Compila tutti i campi obbligatori.", "error");
        return;
    }

    const btn = document.getElementById("btnSaveBooking");
    const originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = "Salvataggio...";

    try {
        if (editingBookingId) {
            await updateBooking(editingBookingId, payload);
            showBookingToast("Prenotazione aggiornata.");
        } else {
            await createBooking(payload);
            showBookingToast("Prenotazione creata.");
        }

        bookingModal.hide();
        await loadBookings();
    } catch (err) {
        showBookingToast(err.message || "Errore durante il salvataggio.", "error");
    } finally {
        btn.disabled = false;
        btn.textContent = originalText;
    }
}

async function handleExportBookings() {
    const btn = document.getElementById("btnExportBookings");
    const originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = "Esportazione...";

    try {
        const date = document.getElementById("filterDate").value || null;
        const res = await downloadBookingsReport(date);
        const blob = new Blob([res.content], { type: "text/csv;charset=utf-8;" });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = res.filename || "bookings.csv";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        showBookingToast("File esportato.");
    } catch (err) {
        showBookingToast(err.message || "Errore durante l'export.", "error");
    } finally {
        btn.disabled = false;
        btn.textContent = originalText;
    }
}

function initBookingThemeToggle() {
    const btn = document.getElementById("btnToggleTheme");
    if (!btn) return;

    const applyTheme = (dark) => {
        document.body.classList.toggle("dark-theme", dark);
        btn.textContent = dark ? "Tema chiaro" : "Tema scuro";
    };

    const saved = localStorage.getItem("bookings-theme");
    const isDark = saved === "dark" || !saved;
    applyTheme(isDark);

    btn.addEventListener("click", () => {
        const nowDark = !document.body.classList.contains("dark-theme");
        applyTheme(nowDark);
        localStorage.setItem("bookings-theme", nowDark ? "dark" : "light");
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const btnAdd = document.getElementById("btnAddBooking");
    if (btnAdd) btnAdd.addEventListener("click", () => openBookingModal(null));

    const bookingForm = document.getElementById("bookingForm");
    if (bookingForm) bookingForm.addEventListener("submit", handleBookingFormSubmit);

    const btnExport = document.getElementById("btnExportBookings");
    if (btnExport) btnExport.addEventListener("click", handleExportBookings);

    initBookingThemeToggle();
});

window.openBookingModal = openBookingModal;
window.showBookingToast = showBookingToast;
