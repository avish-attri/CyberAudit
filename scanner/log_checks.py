from pathlib import Path

from scanner.utils import build_result


def check_failed_logins():
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
        with log_path.open("r", encoding="utf-8", errors="ignore") as file:
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