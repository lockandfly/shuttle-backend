let shuttleModal = null;

document.addEventListener("DOMContentLoaded", () => {
    shuttleModal = new bootstrap.Modal(document.getElementById("shuttleModal"));

    document.getElementById("btnThemeToggle").addEventListener("click", toggleTheme);
    document.getElementById("btnExportXlsx").addEventListener("click", exportXlsx);

    document.getElementById("btnOpenAddModal").addEventListener("click", () => openShuttleModal());
    document.getElementById("shuttleForm").addEventListener("submit", handleShuttleFormSubmit);
});

function toggleTheme() {
    document.body.classList.toggle("light-mode");
}

function showToast(message, type = "success") {
    const container = document.getElementById("toastContainer");
    const id = "toast-" + Date.now();

    const bg = type === "success" ? "bg-success" :
               type === "error" ? "bg-danger" : "bg-secondary";

    container.insertAdjacentHTML("beforeend", `
        <div id="${id}" class="toast text-white ${bg} border-0 mb-2" role="alert">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `);

    const toast = new bootstrap.Toast(document.getElementById(id), { delay: 3000 });
    toast.show();
}

function openShuttleModal(shuttle = null) {
    document.getElementById("formError").classList.add("d-none");

    document.getElementById("shuttleModalTitle").textContent =
        shuttle ? "Modifica navetta" : "Nuova navetta";

    document.getElementById("shuttleId").value = shuttle?.Id || "";
    document.getElementById("shuttleDate").value = shuttle?.Date || "";
    document.getElementById("shuttleTime").value = shuttle?.Time || "";
    document.getElementById("shuttleDestination").value = shuttle?.Destination || "";

    shuttleModal.show();
}

async function handleShuttleFormSubmit(e) {
    e.preventDefault();

    const id = document.getElementById("shuttleId").value;
    const date = document.getElementById("shuttleDate").value;
    const time = document.getElementById("shuttleTime").value;
    const destination = document.getElementById("shuttleDestination").value;

    const errorEl = document.getElementById("formError");

    if (!date || !time || !destination) {
        errorEl.textContent = "Compila tutti i campi.";
        errorEl.classList.remove("d-none");
        return;
    }

    let result = id
        ? await updateShuttle(id, date, time, destination)
        : await createShuttle(date, time, destination);

    if (result.error) {
        errorEl.textContent = result.error;
        errorEl.classList.remove("d-none");
        return;
    }

    shuttleModal.hide();
    showToast("Navetta salvata.");
    loadShuttles();
    refreshCharts();
}

function exportXlsx() {
    const date = document.getElementById("filterDate").value;
    const url = new URL(API_BASE_URL + "/report/xlsx");
    if (date) url.searchParams.append("date", date);
    window.open(url.toString(), "_blank");
}
