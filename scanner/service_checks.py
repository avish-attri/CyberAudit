import subprocess

from scanner.utils import build_result


def check_ssh_service():
    try:
        result = subprocess.run(
            ["systemctl", "is-active", "ssh"],
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
                    "service": "ssh",
                    "status": "active",
                    "reason": "SSH service exposed",
                },
            )

        return build_result(
            "SERVICE-SSH",
            "SSH Service Status",
            "pass",
            {
                "service": "ssh",
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

        services = result.stdout.splitlines()
        count = len(services)
        status = "pass"

        if count > 150:
            status = "warn"

        return build_result(
            "SERVICE-RUNNING-COUNT",
            "Running Services Count",
            status,
            {
                "running_services": count,
            },
        )
    except Exception as e:
        return build_result(
            "SERVICE-RUNNING-COUNT",
            "Running Services Count",
            "unknown",
            {
                "error": str(e),
            },
        )
