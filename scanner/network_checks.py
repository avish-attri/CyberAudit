from scanner.utils import run_command


def check_open_ports():
    """
    Detect open listening ports.
    """
    result = run_command("ss -tuln")
    if not result["success"]:
        return {
            "name": "Open Ports",
            "status": "ERROR",
            "risk": "Unknown",
            "details": result["error"],
            "recommendation": "Check ss command",
        }

    output = result["output"]
    lines = output.split("\n")
    port_count = max(len(lines) - 1, 0)

    if port_count <= 5:
        status = "PASS"
        risk = "Low"
    elif port_count <= 10:
        status = "WARNING"
        risk = "Medium"
    else:
        status = "FAIL"
        risk = "High"

    return {
        "name": "Open Ports",
        "status": status,
        "risk": risk,
        "details": f"Detected {port_count} listening ports",
        "recommendation": "Close unnecessary ports",
    }


def check_firewall_status():
    """
    Check if UFW firewall is active.
    """
    result = run_command("ufw status")
    if not result["success"]:
        return {
            "name": "Firewall Status",
            "status": "WARNING",
            "risk": "Medium",
            "details": "Unable to determine firewall status",
            "recommendation": "Install or configure UFW",
        }

    output = result["output"]
    if "Status: active" in output:
        return {
            "name": "Firewall Status",
            "status": "PASS",
            "risk": "Low",
            "details": "Firewall is active",
            "recommendation": "No action needed",
        }

    return {
        "name": "Firewall Status",
        "status": "FAIL",
        "risk": "High",
        "details": "Firewall is inactive",
        "recommendation": "Enable UFW firewall",
    }
