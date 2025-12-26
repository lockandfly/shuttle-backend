// Aggiorna qui l'URL se necessario
const API_BASE_URL = "https://glowing-goggles-x57xpr7p7pxp3vvg5-8000.app.github.dev";

async function bookingsApiRequest(method, path, params = null) {
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

async function fetchBookings(date = null) {
    return bookingsApiRequest("GET", "/bookings", date ? { date } : null);
}

async function createBooking(payload) {
    return bookingsApiRequest("POST", "/bookings", payload);
}

async function updateBooking(id, payload) {
    return bookingsApiRequest("PUT", `/bookings/${id}`, payload);
}

async function deleteBookingById(id) {
    return bookingsApiRequest("DELETE", `/bookings/${id}`);
}

async function downloadBookingsReport(date = null) {
    const fullUrl = new URL(API_BASE_URL + "/bookings/report/xlsx");
    if (date) fullUrl.searchParams.append("date", date);
    const res = await fetch(fullUrl.toString());
    if (!res.ok) throw new Error(`Export error ${res.status}`);
    return res.json();
}
