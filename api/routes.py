from flask import Blueprint, jsonify, request

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
