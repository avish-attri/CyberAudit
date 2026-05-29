from flask import Blueprint, jsonify, request

from api.pdf_report import save_scan_pdf
from scanner.main import build_scan_report

api_bp = Blueprint("api", __name__)

latest_report = {}


@api_bp.route("/api/scan", methods=["POST"])
def run_scan():
    global latest_report
    latest_report = build_scan_report()
    return jsonify(latest_report)


@api_bp.route("/api/results", methods=["GET"])
def get_results():
    return jsonify(latest_report)


@api_bp.route("/api/reports/pdf", methods=["POST"])
def export_scan_pdf():
    global latest_report
    payload = request.get_json(silent=True) or {}
    report = payload.get("report") or latest_report
    if not report or not report.get("results"):
        return jsonify({"error": "No scan results available to export."}), 400

    try:
        saved_path = save_scan_pdf(report)
    except Exception as exc:
        return jsonify({"error": f"Failed to generate PDF: {exc}"}), 500

    return jsonify(
        {
            "message": "Report saved as PDF.",
            "filename": saved_path.name,
            "path": str(saved_path),
        }
    )
