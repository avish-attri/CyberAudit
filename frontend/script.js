const scanBtn = document.getElementById("scanBtn");
const output = document.getElementById("output");
const lastScanValue = document.getElementById("lastScanValue");
const totalChecksValue = document.getElementById("totalChecksValue");

// Set dark mode
document.documentElement.setAttribute("data-theme", "dark");

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

function renderReport(report) {
    const results = Array.isArray(report.results) ? report.results : [];
    const counts = {
        PASS: 0,
        WARNING: 0,
        FAIL: 0,
        ERROR: 0
    };

    for (const item of results) {
        const status = item.status || "ERROR";
        if (counts[status] !== undefined) {
            counts[status] += 1;
        } else {
            counts.ERROR += 1;
        }
    }

    const cardsHtml = results.map((item) => {
        const status = escapeHtml(item.status || "ERROR");
        const risk = escapeHtml(item.risk || "Unknown");
        const name = escapeHtml(item.name || "Unnamed Check");
        const details = escapeHtml(item.details || "No details provided");
        const recommendation = escapeHtml(item.recommendation || "No recommendation provided");

        return `
            <article class="check-card">
                <div class="card-header">
                    <h3>${name}</h3>
                    <span class="status-badge status-${status.toLowerCase()}">${status}</span>
                </div>
                <p><strong>Risk:</strong> ${risk}</p>
                <p><strong>Details:</strong> ${details}</p>
                <p><strong>Recommendation:</strong> ${recommendation}</p>
            </article>
        `;
    }).join("");

    const now = new Date().toLocaleString();
    lastScanValue.textContent = now;
    totalChecksValue.textContent = String(results.length);

    output.innerHTML = `
        <section class="summary-card">
            <h2>Scan Summary</h2>
            <div class="score-row">
                <span class="score-label">Security Score</span>
                <span class="score-value">${escapeHtml(report.score ?? 0)}%</span>
            </div>
            <div class="status-grid">
                <div class="status-item pass">PASS: ${counts.PASS}</div>
                <div class="status-item warning">WARNING: ${counts.WARNING}</div>
                <div class="status-item fail">FAIL: ${counts.FAIL}</div>
                <div class="status-item error">ERROR: ${counts.ERROR}</div>
            </div>
        </section>
        <section class="checks-section">
            ${cardsHtml || "<p>No checks were returned.</p>"}
        </section>
    `;
}

scanBtn.addEventListener("click", async () => {
    output.innerHTML = '<p class="loading">Running scan...</p>';
    try {
        const response = await fetch("http://127.0.0.1:5000/api/scan", {
            method: "POST"
        });
        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }
        const data = await response.json();
        renderReport(data);
    } catch (error) {
        output.innerHTML = `<p class="error">Error: ${escapeHtml(error.message)}</p>`;
    }
});
