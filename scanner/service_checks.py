import subprocess
from scanner.utils import build_result

def check_ssh_service():
    for unit in ("ssh", "sshd"):
        try:
            result = subprocess.run(
                ["systemctl", "is-active", unit],
                capture_output=True,
                text=True,
            )

            status_output = result.stdout.strip()
            if status_output == "active":
                return build_result(
                    "SERVICE-SSH",
                    "SSH Service Status",
                    "warn",
                    {
                        "service": unit,
                        "status": "active",
                        "reason": "SSH service exposed",
                    },
                )

            if status_output in {"inactive", "failed", "activating", "deactivating"}:
                return build_result(
                    "SERVICE-SSH",
                    "SSH Service Status",
                    "pass",
                    {
                        "service": unit,
                        "status": status_output,
                    },
                )
            
            if status_output == "unknown":
                continue

            return build_result(
                "SERVICE-SSH",
                "SSH Service Status",
                "pass",
                {
                    "service": unit,
                    "status": status_output,
                },
            )
        except Exception as e:
            return build_result(
                "SERVICE-SSH",
                "SSH Service Status",
                "unknown",
                {
                    "error": str(e),
                },
            )

    return build_result(
        "SERVICE-SSH",
        "SSH Service Status",
        "unknown",
        {
            "service": "ssh",
            "reason": "SSH service unit not found",
        },
    )

def check_running_services():

    try:
        result = subprocess.run(
            [
                "systemctl",
                "list-units",
                "--type=service",
                "--state=running",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return build_result(
                "SERVICE-RUNNING-COUNT",
                "Running Services Count",
                "ERROR",
                {
                    "error": result.stderr
                }
            )

        services = [
            line for line in result.stdout.splitlines()
            if ".service" in line
        ]

        count = len(services)
        status = "PASS"

        if count > 150:
            status = "WARNING"

        return build_result(
            "SERVICE-RUNNING-COUNT",
            "Running Services Count",
            status,
            {
                "count": count,
                "sample": services[:5],
            },
        )

    except Exception as e:

        return build_result(
            "SERVICE-RUNNING-COUNT",
            "Running Services Count",
            "ERROR",
            {
                "error": str(e),
            },
        )