import platform
import re
import shutil
import subprocess
from scanner.utils import build_result, run_command

LATEST_KERNEL = "6.8.0"
LATEST_WINDOWS_BUILD = "10.0.22631"

def check_kernel_version():

    if platform.system() == "Windows":

        result = run_command("ver")

        if not result["success"]:
            return build_result(
                "SYS-KERNEL",
                "Kernel Version",
                "ERROR",
                {
                    "error": result.get("error")
                },
            )

        match = re.search(
            r"(\d+\.\d+\.\d+)",
            result["output"],
        )

        if not match:

            return build_result(
                "SYS-KERNEL",
                "Kernel Version",
                "ERROR",
                {
                    "details": "Could not determine Windows version"
                },
            )

        current_version = match.group(1)

        current_parts = [
            int(x)
            for x in current_version.split(".")
        ]

        latest_parts = [
            int(x)
            for x in LATEST_WINDOWS_BUILD.split(".")
        ]

        if current_parts < latest_parts:

            return build_result(
                "SYS-KERNEL",
                "Kernel Version",
                "WARNING",
                {
                    "details":
                    f"Installed Windows version "
                    f"{current_version} is older than "
                    f"recommended version "
                    f"{LATEST_WINDOWS_BUILD}"
                },
            )

        return build_result(
            "SYS-KERNEL",
            "Kernel Version",
            "PASS",
            {
                "details":
                f"Installed Windows version: "
                f"{current_version}"
            },
        )

    # LINUX

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

    current_parts = [
        int(x)
        for x in current_kernel.split(".")
    ]

    latest_parts = [
        int(x)
        for x in LATEST_KERNEL.split(".")
    ]

    if current_parts < latest_parts:

        return build_result(
            "SYS-KERNEL",
            "Kernel Version",
            "WARNING",
            {
                "details":
                f"Installed kernel {current_kernel} "
                f"is older than recommended "
                f"version {LATEST_KERNEL}"
            }
        )

    return build_result(
        "SYS-KERNEL",
        "Kernel Version",
        "PASS",
        {
            "details":
            f"Installed kernel version: "
            f"{current_kernel}"
        }
    )


def check_pending_updates():

    if platform.system() == "Windows":

        result = run_command(
            'sc query wuauserv'
        )

        if not result["success"]:

            return build_result(
                "SYS-UPDATES",
                "Pending Updates",
                "UNKNOWN",
                {
                    "details":
                    "Unable to determine Windows Update status"
                },
            )

        output = (
            result["output"] +
            result["error"]
        ).upper()

        if "RUNNING" in output:

            return build_result(
                "SYS-UPDATES",
                "Pending Updates",
                "PASS",
                {
                    "details":
                    "Windows Update service is running"
                },
            )

        return build_result(
            "SYS-UPDATES",
            "Pending Updates",
            "WARNING",
            {
                "details":
                "Windows Update service is not running"
            },
        )

    result = run_command(
        "apt list --upgradable 2>/dev/null"
    )

    if not result["success"]:

        return build_result(
            "SYS-UPDATES",
            "Pending Updates",
            "ERROR",
            {
                "error": result.get("error")
            }
        )

    lines = result["output"].split("\n")

    updates = max(len(lines) - 1, 0)

    if updates == 0:

        return build_result(
            "SYS-UPDATES",
            "Pending Updates",
            "PASS",
            {
                "details": "System is up to date"
            }
        )

    return build_result(
        "SYS-UPDATES",
        "Pending Updates",
        "WARNING",
        {
            "details":
            f"{updates} packages can be upgraded"
        }
    )


def check_disk_usage():

    path = "C:\\" if platform.system() == "Windows" else "/"

    total, used, free = shutil.disk_usage(path)

    used_percent = round(
        (used / total) * 100,
        2,
    )

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
            "free_gb": round(
                free / (1024**3),
                2,
            ),
        },
    )


def check_security_updates():

    if platform.system() == "Windows":

        result = run_command(
            "sc query wscsvc"
        )

        if not result["success"]:

            return build_result(
                "SYSTEM-SECURITY-UPDATES",
                "Security Updates",
                "UNKNOWN",
                {
                    "details":
                    "Unable to determine Windows security status"
                },
            )

        output = (
            result["output"] +
            result["error"]
        ).upper()

        if "RUNNING" in output:

            return build_result(
                "SYSTEM-SECURITY-UPDATES",
                "Security Updates",
                "PASS",
                {
                    "details":
                    "Windows Security Center service is running"
                },
            )

        return build_result(
            "SYSTEM-SECURITY-UPDATES",
            "Security Updates",
            "WARNING",
            {
                "details":
                "Windows Security Center service is not running"
            },
        )

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

        status = "PASS"

        if len(security_updates) > 0:
            status = "WARNING"

        return build_result(
            "SYSTEM-SECURITY-UPDATES",
            "Security Updates",
            status,
            {
                "security_updates_count":
                len(security_updates),
            },
        )

    except Exception as e:

        return build_result(
            "SYSTEM-SECURITY-UPDATES",
            "Security Updates",
            "UNKNOWN",
            {
                "error": str(e),
            },
        )