from pathlib import Path

from flask import Flask, send_from_directory
from flask_cors import CORS

from api.routes import api_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(api_bp)

FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"


def _resolve_frontend_file(filename: str) -> Path | None:
    direct = FRONTEND_DIR / filename
    if direct.is_file():
        return direct

    parts = Path(filename).parts
    current = FRONTEND_DIR
    resolved_parts: list[str] = []

    for part in parts:
        if not current.is_dir():
            return None

        exact = current / part
        if exact.exists():
            resolved_parts.append(part)
            current = exact if exact.is_dir() else exact.parent
            if exact.is_file():
                return FRONTEND_DIR.joinpath(*resolved_parts)
            continue

        match = next(
            (entry for entry in current.iterdir() if entry.name.lower() == part.lower()),
            None,
        )
        if match is None:
            return None
        resolved_parts.append(match.name)
        current = match if match.is_dir() else match.parent
        if match.is_file():
            return FRONTEND_DIR.joinpath(*resolved_parts)

    candidate = FRONTEND_DIR.joinpath(*resolved_parts)
    return candidate if candidate.is_file() else None


@app.route("/scan", methods=["GET"])
def serve_scan():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/scan-results", methods=["GET"])
def serve_scan_result():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/frontend/<path:filename>", methods=["GET"])
def serve_frontend_file(filename):
    resolved = _resolve_frontend_file(filename)
    if resolved is None:
        return {"error": "File not found"}, 404
    return send_from_directory(resolved.parent, resolved.name)


if __name__ == "__main__":
    print("Starting CyberAudit - Security Audit Tool on http://127.0.0.1:5000/scan")
    app.run(host="127.0.0.1", port=5000, debug=False)
