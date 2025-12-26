// API base - aggiorna se necessario
const API_BASE_URL = "https://glowing-goggles-x57xpr7p7pxp3vvg5-8000.app.github.dev";

async function apiRequest(method, path, params = null) {
    const url = API_BASE_URL + path;
    const options = {
        method,
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    };

    if (method === "GET" || method === "DELETE") {
        const fullUrl = new URL(url);
        if (params) {
            Object.entries(params).forEach(([k, v]) => {
                if (v !== null && v !== undefined && v !== "") {
                    fullUrl.searchParams.append(k, v);
                }
            });
        }
        const res = await fetch(fullUrl.toString(), { method, headers: { "Accept": "application/json" } });
        if (!res.ok) throw new Error(`API error ${res.status}`);
        return res.json();
    }

    // POST / PUT -> JSON body
    if (method === "POST" || method === "PUT") {
        options.body = JSON.stringify(params || {});
    }

    const res = await fetch(url, options);
    if (!res.ok) {
        let msg = `API error ${res.status}`;
        try {
            const j = await res.json();
            if (j && j.detail) msg = j.detail;
        } catch (_) {}
        throw new Error(msg);
    }
    return res.json();
}

async function fetchShuttles(date = null) {
    return apiRequest("GET", "/shuttles", date ? { date } : null);
}

async function createShuttle(date, time, destination) {
    return apiRequest("POST", "/shuttles", { date, time, destination });
}

async function updateShuttle(id, date, time, destination) {
    return apiRequest("PUT", `/shuttles/${id}`, { date, time, destination });
}

async function deleteShuttleById(id) {
    return apiRequest("DELETE", `/shuttles/${id}`);
}

async function downloadXlsx(date = null) {
    const url = new URL(API_BASE_URL + "/report/xlsx");
    if (date) url.searchParams.append("date", date);
    const res = await fetch(url.toString());
    if (!res.ok) throw new Error(`Export error ${res.status}`);
    return res.json();
}
