from flask import Blueprint, jsonify, request

from scanner.main import build_scan_report

api_bp = Blueprint("api", __name__)

latest_report = {}


@api_bp.route("/api/scan", methods=["POST"])
def run_scan():
    global latest_report
    payload = None
    if request.is_json:
        payload = request.get_json(silent=True) or {}
    else:
        payload = {}
    sudo_password = payload.get("sudo_password")
    latest_report = build_scan_report(sudo_password=sudo_password)
    return jsonify(latest_report)


@api_bp.route("/api/results", methods=["GET"])
def get_results():
    return jsonify(latest_report)
