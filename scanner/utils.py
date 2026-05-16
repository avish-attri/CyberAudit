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
    def format_data_details(data_value):
        if isinstance(data_value, dict):
            if data_value.get("reason"):
                return str(data_value.get("reason"))
            if data_value.get("error"):
                return str(data_value.get("error"))
            if data_value.get("details"):
                return str(data_value.get("details"))
            if "used_percent" in data_value and "free_gb" in data_value:
                return f"{data_value['used_percent']}% used, {data_value['free_gb']} GB free"
            if "security_updates_count" in data_value:
                count = data_value["security_updates_count"]
                return "No security updates available" if count == 0 else f"{count} security update(s) available"
            if data_value.get("count") is not None and data_value.get("sample") is not None:
                count = data_value["count"]
                sample_values = data_value["sample"]
                sample_text = ", ".join(str(x) for x in sample_values[:5])
                return f"{count} items found. Sample: {sample_text}"
            return ", ".join(
                f"{key.replace("_", " ").capitalize()}: {value}"
                for key, value in data_value.items()
            )
        if isinstance(data_value, list):
            return ", ".join(str(x) for x in data_value[:5])
        return str(data_value)

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

    details = data.get("reason") or data.get("error") or data.get("details") or format_data_details(data)
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
