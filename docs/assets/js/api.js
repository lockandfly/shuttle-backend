// Configura qui l'URL del tuo backend FastAPI
const API_BASE_URL = "https://glowing-goggles-x57xpr7p7pxp3vvg5-8000.app.github.dev";

async function apiGet(path, params = {}) {
    const url = new URL(API_BASE_URL + path);
    Object.entries(params).forEach(([k, v]) => {
        if (v !== null && v !== undefined && v !== "") {
            url.searchParams.append(k, v);
        }
    });

    const res = await fetch(url, {
        method: "GET",
        headers: {
            "Accept": "application/json"
        }
    });

    if (!res.ok) {
        throw new Error(`GET ${path} failed: ${res.status}`);
    }

    return await res.json();
}

async function apiPost(path, params = {}) {
    const url = new URL(API_BASE_URL + path);
    Object.entries(params).forEach(([k, v]) => {
        if (v !== null && v !== undefined && v !== "") {
            url.searchParams.append(k, v);
        }
    });

    const res = await fetch(url, {
        method: "POST",
        headers: {
            "Accept": "application/json"
        }
    });

    if (!res.ok) {
        throw new Error(`POST ${path} failed: ${res.status}`);
    }

    return await res.json();
}

async function apiPut(path, params = {}) {
    const url = new URL(API_BASE_URL + path);
    Object.entries(params).forEach(([k, v]) => {
        if (v !== null && v !== undefined && v !== "") {
            url.searchParams.append(k, v);
        }
    });

    const res = await fetch(url, {
        method: "PUT",
        headers: {
            "Accept": "application/json"
        }
    });

    if (!res.ok) {
        throw new Error(`PUT ${path} failed: ${res.status}`);
    }

    return await res.json();
}

async function apiDelete(path) {
    const url = new URL(API_BASE_URL + path);

    const res = await fetch(url, {
        method: "DELETE",
        headers: {
            "Accept": "application/json"
        }
    });

    if (!res.ok) {
        throw new Error(`DELETE ${path} failed: ${res.status}`);
    }

    return await res.json();
}

// Wrapper specifici

async function fetchShuttles(date = null) {
    return await apiGet("/shuttles", date ? { date } : {});
}

async function createShuttle(date, time, destination) {
    return await apiPost("/shuttles", { date, time, destination });
}

async function updateShuttle(id, date, time, destination) {
    return await apiPut(`/shuttles/${encodeURIComponent(id)}`, { date, time, destination });
}

async function deleteShuttleById(id) {
    return await apiDelete(`/shuttles/${encodeURIComponent(id)}`);
}
