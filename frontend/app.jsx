const { useEffect, useMemo, useState } = React;

function countStatuses(results) {
    const counts = { PASS: 0, WARNING: 0, FAIL: 0, ERROR: 0 };
    for (const item of results) {
        const status = item?.status;
        if (counts[status] !== undefined) {
            counts[status] += 1;
        } else {
            counts.ERROR += 1;
        }
    }
    return counts;
}

function DashboardApp() {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");
    const [report, setReport] = useState(null);
    const [lastScan, setLastScan] = useState("Not yet run");

    const getRouteFromPath = () => {
        const path = window.location.pathname.replace(/\/+$/, "");
        return path === "/scan-result" || path === "/scan-results" ? "result" : "scan";
    };

    const [route, setRoute] = useState(getRouteFromPath);

    useEffect(() => {
        document.documentElement.setAttribute("data-theme", "dark");

        const onPopState = () => {
            setRoute(getRouteFromPath());
        };

        window.addEventListener("popstate", onPopState);
        return () => window.removeEventListener("popstate", onPopState);
    }, []);

    const results = report?.results ?? [];
    const statusCounts = useMemo(() => countStatuses(results), [results]);
    const chartSeries = useMemo(() => ([
        { key: "PASS", label: "PASS", count: statusCounts.PASS, className: "pass" },
        { key: "WARNING", label: "WARNING", count: statusCounts.WARNING, className: "warning" },
        { key: "FAIL", label: "FAIL", count: statusCounts.FAIL, className: "fail" },
        { key: "ERROR", label: "ERROR", count: statusCounts.ERROR, className: "error" }
    ]), [statusCounts]);
    const totalChecks = results.length;
    const sortedResults = useMemo(() => {
        const order = { FAIL: 1, ERROR: 2, WARNING: 3, PASS: 4 };
        return [...results].sort((a, b) => {
            const aStatus = (a.status || "ERROR").toUpperCase();
            const bStatus = (b.status || "ERROR").toUpperCase();
            return (order[aStatus] || 99) - (order[bStatus] || 99);
        });
    }, [results]);

    const navigate = (path) => {
        window.history.pushState({}, "", path);
        setRoute(getRouteFromPath());
    };

    async function runScan() {
        setError("");
        setIsLoading(true);
        try {
            const response = await fetch("http://127.0.0.1:5000/api/scan", {
                method: "POST"
            });
            if (!response.ok) {
                throw new Error(`Request failed with status ${response.status}`);
            }
            const data = await response.json();
            setReport(data);
            setLastScan(new Date().toLocaleString());
            navigate("/scan-results");
        } catch (err) {
            setError(err?.message || "Failed to run scan");
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="container">
                <header className="topbar">
                    <div>
                        <h1>Linux Security Audit Dashboard</h1>
                        <p className="subtitle">
                            Run checks and review your host security posture quickly.
                        </p>
                    </div>
                    <div className="topbar-actions">
                        <button type="button" onClick={runScan} disabled={isLoading}>
                            {isLoading ? "Scanning..." : route === "result" ? "Rescan" : "Run Scan"}
                        </button>
                    </div>
                </header>

                <section className="meta-panel">
                    <div className="meta-item">
                        <span>Last Scan:</span> <strong>{lastScan}</strong>
                    </div>
                    <div className="meta-item">
                        <span>Total Checks:</span> <strong>{results.length || "-"}</strong>
                    </div>
                </section>

                <div className="results-output">
                    {!report && !isLoading && !error && (
                        <p className="loading">Click "Run Scan" to start.</p>
                    )}

                    {isLoading && (
                        <p className="loading">Running scan...</p>
                    )}

                    {error && (
                        <p className="error">Error: {error}</p>
                    )}

                    {report && !isLoading && !error && (
                        <>
                            <section className="summary-card">
                                <h2>Scan Summary</h2>
                                <div className="score-row">
                                    <span className="score-label">Security Score</span>
                                    <span className="score-value">{report.score ?? 0}%</span>
                                </div>
                                <div className="status-grid">
                                    <div className="status-item pass">PASS: {statusCounts.PASS}</div>
                                    <div className="status-item warning">WARNING: {statusCounts.WARNING}</div>
                                    <div className="status-item fail">FAIL: {statusCounts.FAIL}</div>
                                    <div className="status-item error">ERROR: {statusCounts.ERROR}</div>
                                </div>
                            </section>

                            <section className="charts-grid">
                                <article className="chart-card">
                                    <h3>Checks by Status</h3>
                                    <div className="bar-chart">
                                        {chartSeries.map((item) => {
                                            const pct = totalChecks ? (item.count / totalChecks) * 100 : 0;
                                            return (
                                                <div className="bar-row" key={item.key}>
                                                    <div className="bar-label">{item.label}</div>
                                                    <div className="bar-track">
                                                        <div
                                                            className={`bar-fill ${item.className}`}
                                                            style={{ width: `${pct}%` }}
                                                        />
                                                    </div>
                                                    <div className="bar-value">{item.count}</div>
                                                </div>
                                            );
                                        })}
                                    </div>
                                </article>
                            </section>

                            <section className="checks-section">
                                {sortedResults.map((item, index) => {
                                    const status = (item.status || "ERROR").toLowerCase();
                                    return (
                                        <article className="check-card" key={`${item.name}-${index}`}>
                                            <div className="card-header">
                                                <h3>{item.name || "Unnamed Check"}</h3>
                                                <span className={`status-badge status-${status}`}>
                                                    {item.status || "ERROR"}
                                                </span>
                                            </div>
                                            <p><strong>Risk:</strong> {item.risk || "Unknown"}</p>
                                            <p><strong>Details:</strong> {item.details || "No details provided"}</p>
                                            <p>
                                                <strong>Recommendation:</strong>{" "}
                                                {item.recommendation || "No recommendation provided"}
                                            </p>
                                        </article>
                                    );
                                })}
                            </section>
                        </>
                    )}
                </div>
        </div>
    );
}

ReactDOM.createRoot(document.getElementById("root")).render(<DashboardApp />);
