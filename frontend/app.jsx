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
        return path === "/scan-results" ? "result" : "scan";
    };

    const [route, setRoute] = useState(getRouteFromPath);
    const [activeTab, setActiveTab] = useState("high");
    const [isChecksOpen, setIsChecksOpen] = useState(true);

    const availableChecks = [
        "Authentication and User Configuration",
        "File and Directory Permissions",
        "Service Validation",
        "Network and Port Security",
        "Log Configuration",
        "System Integrity and Package Status",
        "Firewall and Access Controls",
        "Sudo and Privilege Restrictions",
    ];

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
        { key: "ERROR", label: "UNAVAILABLE", count: statusCounts.ERROR, className: "error" }
    ]), [statusCounts]);
    const totalChecks = results.length;
    const statusIconMap = {
        PASS: "🛡️",
        FAIL: "⚠️",
        WARNING: "🚨",
        ERROR: "❌"
    };

    const formatDuration = (seconds) => {
        if (seconds == null || Number.isNaN(seconds)) {
            return "-";
        }
        return `${seconds.toFixed(2)}s`;
    };

    const getStatusLabel = (item) => {
        const status = (item.status || "ERROR").toUpperCase();
        if (status !== "ERROR") {
            return status;
        }

        const details = (item.details || "").toLowerCase();
        if (/permission denied|access denied|operation not permitted|requires root|must be root/.test(details)) {
            return "PERMISSION REQUIRED";
        }
        if (/not configured|not found|no such file|no such directory|command not found|could not find|missing/.test(details)) {
            return "NOT CONFIGURED";
        }
        return "NOT AVAILABLE";
    };

    const formatDetail = (details) => {
        if (details === null || details === undefined) {
            return "No details provided";
        }

        let text = String(details).trim();
        if (!text) {
            return "No details provided";
        }

        const lines = text.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
        text = lines[0] || text;
        text = text.replace(/\s+/g, " ");

        const normalized = text.toLowerCase();
        if (/sudo: .*password|authentication failed|incorrect password|permission denied|operation not permitted|requires root|must be root/.test(normalized)) {
            return "Permission denied or requires higher privileges";
        }
        if (/no such file or directory|command not found|could not find|missing/.test(normalized)) {
            return "Required file or command is missing";
        }
        if (/not configured|not found/.test(normalized)) {
            return "Required setting is not configured";
        }
        if (/unable to determine firewall status/.test(normalized)) {
            return "Could not determine firewall status";
        }

        return text.length > 90 ? `${text.slice(0, 90)}...` : text;
    };

    const sortedResults = useMemo(() => {
        const order = { FAIL: 1, WARNING: 2, ERROR: 3, PASS: 4 };
        return [...results].sort((a, b) => {
            const aStatus = (a.status || "ERROR").toUpperCase();
            const bStatus = (b.status || "ERROR").toUpperCase();
            return (order[aStatus] || 99) - (order[bStatus] || 99);
        });
    }, [results]);

    const activeTabResults = useMemo(() => {
        const selectedRisk = activeTab === "high"
            ? "high"
            : activeTab === "medium"
                ? "medium"
                : activeTab === "low"
                    ? "low"
                    : activeTab === "unknown"
                        ? "unknown"
                        : null;

        return sortedResults.filter((item) => {
            if (!selectedRisk) {
                return true;
            }
            const itemRisk = (item.risk || "Unknown").toLowerCase();
            return itemRisk === selectedRisk;
        });
    }, [sortedResults, activeTab]);

    const tabIconMap = {
        high: "⚠️",
        medium: "🚨",
        low: "🛡️",
        unknown: "❔",
        all: "📋"
    };

    const navigate = (path) => {
        window.history.pushState({}, "", path);
        setRoute(getRouteFromPath());
    };

    async function runScan() {
        setError("");
        setIsLoading(true);
        try {
            const response = await fetch("http://127.0.0.1:5000/api/scan", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
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
                    <div className="meta-item">
                        <span>Host IP:</span> <strong>{report?.host_ip || "-"}</strong>
                    </div>
                    <div className="meta-item">
                        <span>Scan Time:</span> <strong>{formatDuration(report?.duration_seconds)}</strong>
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
                                    <div className="status-item error">UNAVAILABLE: {statusCounts.ERROR}</div>
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

                            <section className="tabs-panel">
                                {[
                                    { key: "high", label: "High Risk" },
                                    { key: "medium", label: "Medium Risk" },
                                    { key: "low", label: "Low Risk" },
                                    { key: "unknown", label: "Unknown Risk" },
                                    { key: "all", label: "All Checks" },
                                ].map((tab) => (
                                    <button
                                        key={tab.key}
                                        type="button"
                                        className={`tab-btn ${activeTab === tab.key ? "active" : ""}`}
                                        onClick={() => setActiveTab(tab.key)}
                                    >
                                        {tabIconMap[tab.key]} {tab.label}
                                    </button>
                                ))}
                            </section>

                            <section className="checks-section">
                                {activeTabResults.map((item, index) => {
                                    const status = (item.status || "ERROR").toLowerCase();
                                    return (
                                        <article className="check-card" key={`${item.name}-${index}`}>
                                            <div className="card-header">
                                                <h3>{item.name || "Unnamed Check"}</h3>
                                                <span className={`status-badge status-${status}`}>
                                                    {statusIconMap[(item.status || "ERROR").toUpperCase()] || "❔"}
                                                    {" "}{getStatusLabel(item)}
                                                </span>
                                            </div>
                                            <p><strong>Risk:</strong> {item.risk || "Unknown"}</p>
                                            <p><strong>Details:</strong> {formatDetail(item.details)}</p>
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

                {route === "scan" && (
                    <section className="collapsible-panel">
                        <button
                            type="button"
                            className="collapsible-toggle"
                            onClick={() => setIsChecksOpen((prev) => !prev)}
                        >
                            <span>{isChecksOpen ? "▼" : "▶"}</span>
                            <div>
                                <h2>Available Scan Checks</h2>
                                {!isChecksOpen && (
                                    <p className="collapsible-subtitle">Expand to preview the checks performed during a scan.</p>
                                )}
                            </div>
                        </button>
                        {isChecksOpen && (
                            <div className="collapse-content">
                                <ul className="checks-list">
                                    {availableChecks.map((check) => (
                                        <li className="check-list-item" key={check}>{check}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </section>
                )}
        </div>
    );
}

ReactDOM.createRoot(document.getElementById("root")).render(<DashboardApp />);
