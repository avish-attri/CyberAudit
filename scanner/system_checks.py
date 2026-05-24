import shutil
import subprocess

from scanner.utils import build_result, run_command, format_details

LATEST_KERNEL = "6.8.0"

def check_kernel_version():

    result = run_command("uname -r")

    if not result["success"]:
        return build_result(
            "SYS-KERNEL",
            "Kernel Version",
            "ERROR",
            {
                "error": result.get("error")
            }
        )

    current_kernel = result["output"].split("-")[0]

    current_parts = [int(x) for x in current_kernel.split(".")]
    latest_parts = [int(x) for x in LATEST_KERNEL.split(".")]

    if current_parts < latest_parts:

        return build_result(
            "SYS-KERNEL",
            "Kernel Version",
            "WARNING",
            {
                "details": f"Installed kernel {current_kernel} is older than recommended version {LATEST_KERNEL}"
            }
        )

    return build_result(
        "SYS-KERNEL",
        "Kernel Version",
        "PASS",
        {
            "details": f"Installed kernel version: {current_kernel}"
        }
    )


def check_pending_updates():

    result = run_command("apt list --upgradable 2>/dev/null")
    if not result["success"]:
        return {
            "name": "Pending Updates",
            "status": "ERROR",
            "risk": "Unknown",
            "details": format_details(result.get("error")),
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


def check_disk_usage():
    total, used, free = shutil.disk_usage("/")
    used_percent = round((used / total) * 100, 2)
    status = "pass"
    if used_percent >= 90:
        status = "fail"
    elif used_percent >= 75:
        status = "warn"

    return build_result(
        "SYSTEM-DISK-USAGE",
        "Root Disk Usage",
        status,
        {
            "used_percent": used_percent,
            "free_gb": round(free / (1024**3), 2),
        },
    )


def check_security_updates():
    try:
        result = subprocess.run(
            ["apt", "list", "--upgradable"],
            capture_output=True,
            text=True,
        )

        output = result.stdout.lower()
        security_updates = []
        for line in output.splitlines():
            if "security" in line:
                security_updates.append(line)

        status = "pass"
        if len(security_updates) > 0:
            status = "warn"

        return build_result(
            "SYSTEM-SECURITY-UPDATES",
            "Security Updates",
            status,
            {
                "security_updates_count": len(security_updates),
            },
        )
    except Exception as e:
        return build_result(
            "SYSTEM-SECURITY-UPDATES",
            "Security Updates",
            "unknown",
            {
                "error": str(e),
            },
        )
