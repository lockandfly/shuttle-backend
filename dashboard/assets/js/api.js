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
        const response = await fetch(fullUrl.toString(), options);
        return response.json();
    }

    // POST e PUT → body JSON
    if (method === "POST" || method === "PUT") {
        options.body = JSON.stringify(params || {});
    }

    const response = await fetch(url, options);
    return response.json();
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
    return fetch(url.toString());
}
