let shuttleModal = null;

document.addEventListener("DOMContentLoaded", () => {
    shuttleModal = new bootstrap.Modal(document.getElementById("shuttleModal"));

    document.getElementById("btnThemeToggle").addEventListener("click", toggleTheme);
    document.getElementById("btnExportXlsx").addEventListener("click", exportXlsx);

    document.getElementById("btnOpenAddModal").addEventListener("click", () => openShuttleModal());
    document.getElementById("shuttleForm").addEventListener("submit", handleShuttleFormSubmit);

    initTable();       // in table.js
    loadShuttles();    // in table.js
    initCharts();      // in charts.js
});

function toggleTheme() {
    document.body.classList.toggle("light-mode");
}

function showToast(message, type = "success") {
    const container = document.getElementById("toastContainer");
    const id = "toast-" + Date.now();

    const bgClass = type === "success" ? "bg-success" :
                    type === "error"   ? "bg-danger"  :
                    type === "warning" ? "bg-warning text-dark" : "bg-secondary";

    const html = `
        <div id="${id}" class="toast align-items-center text-white ${bgClass} border-0 mb-2" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    container.insertAdjacentHTML("beforeend", html);

    const toastEl = document.getElementById(id);
    const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
    toast.show();

    toastEl.addEventListener("hidden.bs.toast", () => {
        toastEl.remove();
    });
}

function openShuttleModal(shuttle = null) {
    const titleEl = document.getElementById("shuttleModalTitle");
    const idEl = document.getElementById("shuttleId");
    const dateEl = document.getElementById("shuttleDate");
    const timeEl = document.getElementById("shuttleTime");
    const destEl = document.getElementById("shuttleDestination");
    const errorEl = document.getElementById("formError");

    errorEl.classList.add("d-none");
    errorEl.textContent = "";

    if (shuttle) {
        titleEl.textContent = "Modifica navetta";
        idEl.value = shuttle.Id;
        dateEl.value = shuttle.Date;
        timeEl.value = shuttle.Time;
        destEl.value = shuttle.Destination;
    } else {
        titleEl.textContent = "Nuova navetta";
        idEl.value = "";
        dateEl.value = "";
        timeEl.value = "";
        destEl.value = "";
    }

    shuttleModal.show();
}

async function handleShuttleFormSubmit(event) {
    event.preventDefault();

    const id = document.getElementById("shuttleId").value.trim();
    const date = document.getElementById("shuttleDate").value.trim();
    const time = document.getElementById("shuttleTime").value.trim();
    const destination = document.getElementById("shuttleDestination").value.trim();
    const errorEl = document.getElementById("formError");

    if (!date || !time || !destination) {
        errorEl.textContent = "Compila tutti i campi.";
        errorEl.classList.remove("d-none");
        return;
    }

    try {
        let result;
        if (id) {
            result = await updateShuttle(id, date, time, destination);
        } else {
            result = await createShuttle(date, time, destination);
        }

        if (result.error) {
            errorEl.textContent = result.error;
            errorEl.classList.remove("d-none");
            return;
        }

        shuttleModal.hide();
        showToast("Navetta salvata correttamente.", "success");
        await loadShuttles();
        await refreshCharts();
    } catch (err) {
        console.error(err);
        errorEl.textContent = "Errore durante il salvataggio.";
        errorEl.classList.remove("d-none");
    }
}

async function exportXlsx() {
    const dateFilter = document.getElementById("filterDate").value.trim();
    const url = new URL(API_BASE_URL + "/report/xlsx");
    if (dateFilter) {
        url.searchParams.append("date", dateFilter);
    }
    window.open(url.toString(), "_blank");
}
