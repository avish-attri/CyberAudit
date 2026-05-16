import subprocess


def run_command(command):
    """
    Runs a shell command safely and returns output.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "output": result.stdout.strip(),
            "error": result.stderr.strip(),
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e),
        }


def build_result(check_id, name, status, data):
    normalized = status.upper()
    mapping = {
        "WARN": "WARNING",
        "PASS": "PASS",
        "FAIL": "FAIL",
        "UNKNOWN": "ERROR",
    }
    normalized = mapping.get(normalized, normalized)

    risk_map = {
        "PASS": "Low",
        "WARNING": "Medium",
        "FAIL": "High",
        "ERROR": "Unknown",
    }

    details = data.get("reason") or data.get("error") or data.get("details") or str(data)
    recommendation = "Review system configuration"
    if normalized == "FAIL":
        recommendation = "Remediate the identified security issue"
    elif normalized == "WARNING":
        recommendation = "Investigate and address the warning"
    elif normalized == "ERROR":
        recommendation = "Check the system state and rerun the check"
    elif normalized == "PASS":
        recommendation = "No action needed"

    return {
        "id": check_id,
        "name": name,
        "status": normalized,
        "risk": risk_map.get(normalized, "Unknown"),
        "details": details,
        "recommendation": recommendation,
        "data": data,
    }
