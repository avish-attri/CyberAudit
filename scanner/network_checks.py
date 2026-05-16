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
    Check whether a supported firewall is active.
    """
    ufw_result = run_command("ufw status")
    if ufw_result["success"]:
        output = ufw_result["output"].lower()
        if "status: active" in output or "active" in output:
            return {
                "name": "Firewall Status",
                "status": "PASS",
                "risk": "Low",
                "details": "UFW firewall is active",
                "recommendation": "No action needed",
            }
        return {
            "name": "Firewall Status",
            "status": "FAIL",
            "risk": "High",
            "details": "UFW firewall is inactive",
            "recommendation": "Enable UFW firewall",
        }

    firewalld_result = run_command("firewall-cmd --state")
    if firewalld_result["success"]:
        output = firewalld_result["output"].strip().lower()
        if output == "running":
            return {
                "name": "Firewall Status",
                "status": "PASS",
                "risk": "Low",
                "details": "firewalld is running",
                "recommendation": "No action needed",
            }
        return {
            "name": "Firewall Status",
            "status": "FAIL",
            "risk": "High",
            "details": "firewalld is not running",
            "recommendation": "Start and enable firewalld",
        }

    details = (
        ufw_result["error"] or firewalld_result["error"] or "Unable to determine firewall status"
    )
    return {
        "name": "Firewall Status",
        "status": "WARNING",
        "risk": "Medium",
        "details": details,
        "recommendation": "Install or configure UFW or firewalld with sudo permissions",
    }
