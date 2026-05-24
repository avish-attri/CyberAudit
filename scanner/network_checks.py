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
            "details": f"{port_count} listening ports detected"
        },
    )

def check_firewall_status():

    ufw_result = run_command("ufw status")

    ufw_output = (
        ufw_result.get("output", "") +
        ufw_result.get("error", "")
    ).lower()

    if "you need to be root" in ufw_output or "permission denied" in ufw_output:

        return build_result(
            "NETWORK-FIREWALL",
            "Firewall Status",
            "WARNING",
            {
                "details": "Firewall status requires root privileges"
            },
        )

    if ufw_result["success"]:

        if "status: active" in ufw_output:

            return build_result(
                "NETWORK-FIREWALL",
                "Firewall Status",
                "PASS",
                {
                    "details": "UFW firewall is active"
                },
            )

        if "inactive" in ufw_output:

            return build_result(
                "NETWORK-FIREWALL",
                "Firewall Status",
                "FAIL",
                {
                    "details": "UFW firewall is inactive"
                },
            )

    firewalld_result = run_command("firewall-cmd --state")

    firewalld_output = (
        firewalld_result.get("output", "") +
        firewalld_result.get("error", "")
    ).lower()

    if firewalld_result["success"]:

        if "running" in firewalld_output:

            return build_result(
                "NETWORK-FIREWALL",
                "Firewall Status",
                "PASS",
                {
                    "details": "firewalld is running"
                },
            )

        return build_result(
            "NETWORK-FIREWALL",
            "Firewall Status",
            "FAIL",
            {
                "details": "firewalld is not running"
            },
        )

    return build_result(
        "NETWORK-FIREWALL",
        "Firewall Status",
        "WARNING",
        {
            "details": "Unable to determine firewall status"
        },
    )