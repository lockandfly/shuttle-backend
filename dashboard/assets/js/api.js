const API_BASE_URL = "https://glowing-goggles-x57xpr7p7pxp3vvg5-8000.app.github.dev";

async function apiGet(path, params = {}) {
    const url = new URL(API_BASE_URL + path);
    Object.entries(params).forEach(([k, v]) => v && url.searchParams.append(k, v));

    const res = await fetch(url);
    return await res.json();
}

async function apiPost(path, params = {}) {
    const url = new URL(API_BASE_URL + path);
    Object.entries(params).forEach(([k, v]) => v && url.searchParams.append(k, v));

    const res = await fetch(url, { method: "POST" });
    return await res.json();
}

async function apiPut(path, params = {}) {
    const url = new URL(API_BASE_URL + path);
    Object.entries(params).forEach(([k, v]) => v && url.searchParams.append(k, v));

    const res = await fetch(url, { method: "PUT" });
    return await res.json();
}

async function apiDelete(path) {
    const url = new URL(API_BASE_URL + path);
    const res = await fetch(url, { method: "DELETE" });
    return await res.json();
}

async function fetchShuttles(date = null) {
    return await apiGet("/shuttles", date ? { date } : {});
}

async function createShuttle(date, time, destination) {
    return await apiPost("/shuttles", { date, time, destination });
}

async function updateShuttle(id, date, time, destination) {
    return await apiPut(`/shuttles/${id}`, { date, time, destination });
}

async function deleteShuttleById(id) {
    return await apiDelete(`/shuttles/${id}`);
}
