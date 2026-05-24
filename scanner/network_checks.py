from scanner.utils import run_command, format_details, build_result

def check_open_ports():

    result = run_command("ss -tulnp")

    if not result["success"]:

        return build_result(
            "NETWORK-OPEN-PORTS",
            "Open Ports",
            "ERROR",
            {
                "error": result.get("error")
            }
        )

    services = [
        line for line in result["output"].splitlines()
        if "LISTEN" in line
    ]

    port_count = len(services)
    ports = []

    for line in services:
        parts = line.split()

        # Local Address:Port column
        if len(parts) >= 5:
            ports.append(parts[4])

    status = "PASS"

    if port_count > 10:
        status = "FAIL"

    elif port_count > 5:
        status = "WARNING"

    return build_result(
        "NETWORK-OPEN-PORTS",
        "Open Ports",
        status,
        {
            "count": port_count,
            "sample": ports[:5],
        },
    )

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
        ufw_result.get("error") or firewalld_result.get("error") or "Unable to determine firewall status"
    )
    return {
        "name": "Firewall Status",
        "status": "WARNING",
        "risk": "Medium",
        "details": format_details(details),
        "recommendation": "Install or configure UFW or firewalld with sudo permissions",
    }
