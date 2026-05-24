import os
from scanner.utils import build_result 

def check_auth_logs():
    log_path = "/var/log/auth.log"

    if os.path.exists(log_path):
        return build_result(
            "AUTH-LOGS",
            "Authentication Logs",
            "PASS",
            {
                "details": "Authentication logs found"
            },
        )

    return build_result(
        "AUTH-LOGS",
        "Authentication Logs",
        "WARNING",
        {
            "details": "Authentication logs not found"
        },
    )