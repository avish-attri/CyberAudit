from scanner.utils import run_command


def check_kernel_version():
    """
    Get Linux kernel version.
    """
    result = run_command("uname -r")
    if not result["success"]:
        return {
            "name": "Kernel Version",
            "status": "ERROR",
            "risk": "Unknown",
            "details": result["error"],
            "recommendation": "Check uname command",
        }

    return {
        "name": "Kernel Version",
        "status": "PASS",
        "risk": "Low",
        "details": f"Kernel version: {result['output']}",
        "recommendation": "Keep kernel updated",
    }


def check_pending_updates():
    """
    Check for pending package updates.
    """
    result = run_command("apt list --upgradable 2>/dev/null")
    if not result["success"]:
        return {
            "name": "Pending Updates",
            "status": "ERROR",
            "risk": "Unknown",
            "details": result["error"],
            "recommendation": "Check package manager",
        }

    lines = result["output"].split("\n")
    updates = max(len(lines) - 1, 0)
    if updates == 0:
        return {
            "name": "Pending Updates",
            "status": "PASS",
            "risk": "Low",
            "details": "System is up to date",
            "recommendation": "No action needed",
        }
    return {
        "name": "Pending Updates",
        "status": "WARNING",
        "risk": "Medium",
        "details": f"{updates} packages can be upgraded",
        "recommendation": "Install latest security updates",
    }
