from pathlib import Path

from flask import Flask, send_from_directory
from flask_cors import CORS

from api.routes import api_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(api_bp)

FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"


@app.route("/scan", methods=["GET"])
def serve_scan():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/scan-results", methods=["GET"])
def serve_scan_result():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/frontend/<path:filename>", methods=["GET"])
def serve_frontend_file(filename):
    return send_from_directory(FRONTEND_DIR, filename)


if __name__ == "__main__":
    print("Starting Linux Security Audit Tool...")
    print("Frontend routes available:")
    print("  http://127.0.0.1:5000/scan  -> Scan page")
    print("  http://127.0.0.1:5000/scan-results  -> Results page")
    app.run(debug=True)
