import subprocess
import re

def run_command(command):
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


def format_details(data_value):

    if data_value is None:
        return "No details provided"

    if isinstance(data_value, dict):
        # prefer explicit fields
        if data_value.get("reason"):
            return str(data_value.get("reason"))
        if data_value.get("error"):
            return str(data_value.get("error"))
        if data_value.get("details"):
            return str(data_value.get("details"))
        # common structured payloads
        if "used_percent" in data_value and "free_gb" in data_value:
            return f"{data_value['used_percent']}% used, {data_value['free_gb']} GB free"
        if "security_updates_count" in data_value:
            cnt = data_value.get("security_updates_count", 0)
            return "No security updates available" if cnt == 0 else f"{cnt} security update(s) available"
        if data_value.get("count") is not None and data_value.get("sample") is not None:
            count = data_value.get("count")
            sample = data_value.get("sample") or []
            sample_text = ", ".join(str(x) for x in sample[:5])
            return f"{count} items found. Sample: {sample_text}"
        # fallback: join simple key/value pairs
        try:
            parts = []
            for k, v in data_value.items():
                parts.append(f"{k.replace('_', ' ').capitalize()}: {v}")
            return ", ".join(parts) if parts else "No details provided"
        except Exception:
            return str(data_value)

    if isinstance(data_value, list):
        if not data_value:
            return "No details provided"
        return ", ".join(str(x) for x in data_value[:5])

    # strings or exceptions
    text = str(data_value).strip()
    if not text:
        return "No details provided"

    # collapse whitespace and newlines
    text = " ".join(text.split())

    # remove Windows-specific noise like "[WinError 2]" or "WinError 2"
    try:
        text = re.sub(r"\[winerror[^\]]*\]", "", text, flags=re.IGNORECASE)
        text = re.sub(r"winerror\s*\d+", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\[errno[^\]]*\]", "", text, flags=re.IGNORECASE)
        text = re.sub(r"errno\s*\d+", "", text, flags=re.IGNORECASE)
        text = re.sub(r"^\s*oserror:\s*", "", text, flags=re.IGNORECASE)
        text = text.strip()
    except Exception:
        pass

    low = text.lower()
    if "permission denied" in low or "operation not permitted" in low or "requires root" in low or "authentication failed" in low:
        return "Permission denied or requires higher privileges"
    if "no such file or directory" in low or "command not found" in low or "could not find" in low or "missing" in low:
        return "Required file or command is missing"
    if "unable to determine firewall status" in low:
        return "Could not determine firewall status"

    return text if len(text) <= 120 else text[:117] + "..."


def build_result(check_id, name, status, data):
    
    normalized = status.upper()
    mapping = {
        "WARN": "WARNING",
        "PASS": "PASS",
        "FAIL": "FAIL",
        "UNKNOWN": "ERROR",
        "NOT_AVAILABLE": "NOT_AVAILABLE",
    }
    normalized = mapping.get(normalized, normalized)

    risk_map = {
        "PASS": "Low",
        "WARNING": "Medium",
        "FAIL": "High",
        "ERROR": "Unknown",
        "NOT_AVAILABLE": "Unknown",
    }

    details = data.get("reason") or data.get("error") or data.get("details") or format_details(data)
    recommendation = "Review system configuration"
    if normalized == "FAIL":
        recommendation = "Remediate the identified security issue"
    elif normalized == "WARNING":
        recommendation = "Investigate and address the warning"
    elif normalized == "ERROR":
        recommendation = "Check the system state and rerun the check"
    elif normalized == "PASS":
        recommendation = "No action needed"
    elif normalized == "NOT_AVAILABLE":
        recommendation = "Not applicable on this operating system"

    return {
        "id": check_id,
        "name": name,
        "status": normalized,
        "risk": risk_map.get(normalized, "Unknown"),
        "details": details,
        "recommendation": recommendation,
        "data": data,
    }

def not_available_result(check_id, name):
    return build_result(
        check_id,
        name,
        "NOT_AVAILABLE",
        {
            "details": "This security check is Linux-specific",
        },
    )