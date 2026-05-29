from scanner.utils import run_command, format_details, build_result
import platform

def check_open_ports():

    if platform.system() == "Windows":

        result = run_command(
            'netstat -ano | findstr LISTENING'
        )

        if not result["success"]:

            return build_result(
                "NETWORK-OPEN-PORTS",
                "Open Ports",
                "ERROR",
                {
                    "error": result.get("error")
                }
            )

        services = result["output"].splitlines()

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

    # LINUX
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

    # WINDOWS
    if platform.system() == "Windows":

        result = run_command(
            "netsh advfirewall show allprofiles state"
        )

        if not result["success"]:

            return build_result(
                "NETWORK-FIREWALL",
                "Firewall Status",
                "WARNING",
                {
                    "details": "Unable to determine firewall status"
                },
            )

        output = result["output"].lower()

        # Domain, Private and Public profiles all ON
        if output.count("on") >= 3:

            return build_result(
                "NETWORK-FIREWALL",
                "Firewall Status",
                "PASS",
                {
                    "details": "Windows Firewall is active on all profiles"
                },
            )

        # At least one profile OFF
        if "off" in output:

            return build_result(
                "NETWORK-FIREWALL",
                "Firewall Status",
                "FAIL",
                {
                    "details": "Windows Firewall is disabled on one or more profiles"
                },
            )

        return build_result(
            "NETWORK-FIREWALL",
            "Firewall Status",
            "WARNING",
            {
                "details": "Could not determine Windows Firewall state"
            },
        )

    # LINUX
    ufw_result = run_command("ufw status")

    ufw_output = (
        ufw_result.get("output", "")
        + ufw_result.get("error", "")
    ).lower()

    if (
        "you need to be root" in ufw_output
        or "permission denied" in ufw_output
    ):

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

    firewalld_result = run_command(
        "firewall-cmd --state"
    )

    firewalld_output = (
        firewalld_result.get("output", "")
        + firewalld_result.get("error", "")
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