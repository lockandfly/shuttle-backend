// API base
const API_BASE_URL = "https://glowing-goggles-x57xpr7p7pxp3vvg5-8000.app.github.dev";

// --- Helper generico per le chiamate API ---
async function apiRequest(method, path, params = null) {
    const url = new URL(API_BASE_URL + path);

    // Per GET/DELETE mettiamo i parametri in query string
    if ((method === "GET" || method === "DELETE") && params) {
        Object.entries(params).forEach(([key, value]) => {
            if (value !== null && value !== undefined && value !== "") {
                url.searchParams.append(key, value);
            }
        });
    }

    const options = {
        method,
        headers: {
            "Accept": "application/json"
        }
    };

    // Per POST/PUT usiamo la query string (come nel backend attuale)
    if ((method === "POST" || method === "PUT") && params) {
        Object.entries(params).forEach(([key, value]) => {
            if (value !== null && value !== undefined && value !== "") {
                url.searchParams.append(key, value);
            }
        });
    }

    const response = await fetch(url.toString());

    if (!response.ok) {
        let message = `Errore API (${response.status})`;
        try {
            const data = await response.json();
            if (data && data.error) message = data.error;
        } catch (_) {}
        throw new Error(message);
    }

    // In caso di XLSX o altri formati, gestiamo fuori
    const contentType = response.headers.get("Content-Type") || "";
    if (!contentType.includes("application/json")) {
        return response;
    }

    return response.json();
}

// --- Funzioni specifiche ---

async function fetchShuttles(date = null) {
    return apiRequest("GET", "/shuttles", date ? { date } : null);
}

async function createShuttle(date, time, destination) {
    return apiRequest("POST", "/shuttles", { date, time, destination });
}

async function updateShuttle(id, date, time, destination) {
    const params = {};
    if (date) params.date = date;
    if (time) params.time = time;
    if (destination) params.destination = destination;

    return apiRequest("PUT", `/shuttles/${id}`, params);
}

async function deleteShuttleById(id) {
    return apiRequest("DELETE", `/shuttles/${id}`);
}

async function downloadXlsx(date = null) {
    const url = new URL(API_BASE_URL + "/report/xlsx");
    if (date) url.searchParams.append("date", date);

    const response = await fetch(url.toString());
    if (!response.ok) {
        throw new Error(`Errore export XLSX (${response.status})`);
    }
    return response;
}
