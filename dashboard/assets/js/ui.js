let shuttleModal = null;
let editingShuttleId = null;

function showToast(message, type = "success") {
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

function openShuttleModal(shuttle = null) {
    const modalEl = document.getElementById("shuttleModal");
    if (!shuttleModal) {
        shuttleModal = new bootstrap.Modal(modalEl);
    }

    const titleEl = modalEl.querySelector(".modal-title");
    const dateInput = document.getElementById("shuttleDate");
    const timeInput = document.getElementById("shuttleTime");
    const destInput = document.getElementById("shuttleDestination");

    if (shuttle) {
        editingShuttleId = shuttle.Id;
        titleEl.textContent = "Modifica navetta";
        dateInput.value = shuttle.Date || "";
        timeInput.value = shuttle.Time || "";
        destInput.value = shuttle.Destination || "";
    } else {
        editingShuttleId = null;
        titleEl.textContent = "Nuova navetta";
        dateInput.value = "";
        timeInput.value = "";
        destInput.value = "";
    }

    shuttleModal.show();
}

async function handleShuttleFormSubmit(event) {
    event.preventDefault();

    const date = document.getElementById("shuttleDate").value.trim();
    const time = document.getElementById("shuttleTime").value.trim();
    const destination = document.getElementById("shuttleDestination").value.trim();

    if (!date || !time || !destination) {
        showToast("Compila tutti i campi.", "error");
        return;
    }

    const submitBtn = document.getElementById("btnSaveShuttle");
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = "Salvataggio...";

    try {
        if (editingShuttleId) {
            await updateShuttle(editingShuttleId, date, time, destination);
            showToast("Navetta aggiornata.");
        } else {
            await createShuttle(date, time, destination);
            showToast("Navetta aggiunta.");
        }

        shuttleModal.hide();
        await loadShuttles();
        await refreshCharts();
    } catch (err) {
        showToast(err.message || "Errore durante il salvataggio.", "error");
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
}

async function handleExportXlsx() {
    const btn = document.getElementById("btnExportXlsx");
    const originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = "Esportazione...";

    try {
        const date = document.getElementById("filterDate").value || null;
        const res = await downloadXlsx(date);
        // For simplicity the backend returns CSV content in JSON; create a blob
        const blob = new Blob([res.content], { type: "text/csv;charset=utf-8;" });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = res.filename || "shuttles.csv";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        showToast("File esportato.");
    } catch (err) {
        showToast(err.message || "Errore durante l'export.", "error");
    } finally {
        btn.disabled = false;
        btn.textContent = originalText;
    }
}

function initThemeToggle() {
    const btn = document.getElementById("btnToggleTheme");
    if (!btn) return;
    const applyTheme = (dark) => {
        document.body.classList.toggle("dark-theme", dark);
        btn.textContent = dark ? "Tema chiaro" : "Tema scuro";
    };
    const saved = localStorage.getItem("shuttle-theme");
    const isDark = saved === "dark";
    applyTheme(isDark);
    btn.addEventListener("click", () => {
        const nowDark = !document.body.classList.contains("dark-theme");
        applyTheme(nowDark);
        localStorage.setItem("shuttle-theme", nowDark ? "dark" : "light");
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const btnAdd = document.getElementById("btnAddShuttle");
    if (btnAdd) btnAdd.addEventListener("click", () => openShuttleModal(null));

    const shuttleForm = document.getElementById("shuttleForm");
    if (shuttleForm) shuttleForm.addEventListener("submit", handleShuttleFormSubmit);

    const btnExport = document.getElementById("btnExportXlsx");
    if (btnExport) btnExport.addEventListener("click", handleExportXlsx);

    initThemeToggle();
});

window.openShuttleModal = openShuttleModal;
window.showToast = showToast;
