from pathlib import Path
import platform

from scanner.utils import build_result, run_command


def check_failed_logins():

    # WINDOWS
    if platform.system() == "Windows":

        try:

            result = run_command(
                'powershell "(Get-WinEvent -FilterHashtable @{LogName=\'Security\'; ID=4625} -MaxEvents 100).Count"'
            )

            if not result["success"]:

                return build_result(
                    "LOG-FAILED-LOGINS",
                    "Failed Login Attempts",
                    "unknown",
                    {
                        "error": result.get("error"),
                    },
                )

            failed_count = int(result["output"] or 0)

            status = "pass"

            if failed_count > 20:
                status = "fail"

            elif failed_count > 5:
                status = "warn"

            return build_result(
                "LOG-FAILED-LOGINS",
                "Failed Login Attempts",
                status,
                {
                    "failed_login_count": failed_count,
                },
            )

        except Exception as e:

            return build_result(
                "LOG-FAILED-LOGINS",
                "Failed Login Attempts",
                "unknown",
                {
                    "error": str(e),
                },
            )

    # LINUX
    log_path = Path("/var/log/auth.log")

    if not log_path.exists():

        return build_result(
            "LOG-FAILED-LOGINS",
            "Failed Login Attempts",
            "unknown",
            {
                "reason": "auth.log not found",
            },
        )

    try:

        failed_count = 0

        with log_path.open(
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as file:

            for line in file:

                if "Failed password" in line:
                    failed_count += 1

        status = "pass"

        if failed_count > 20:
            status = "fail"

        elif failed_count > 5:
            status = "warn"

        return build_result(
            "LOG-FAILED-LOGINS",
            "Failed Login Attempts",
            status,
            {
                "failed_login_count": failed_count,
            },
        )

    except Exception as e:

        return build_result(
            "LOG-FAILED-LOGINS",
            "Failed Login Attempts",
            "unknown",
            {
                "error": str(e),
            },
        )