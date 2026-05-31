import os
import platform
from scanner.utils import build_result 

def check_auth_logs():  
    # WINDOWS
    if platform.system() == "Windows":

        log_path = r"C:\Windows\System32\winevt\Logs\Security.evtx"

        if os.path.exists(log_path):

            return build_result(
                "AUTH-LOGS",
                "Authentication Logs",
                "PASS",
                {
                    "details": "Windows Security Event Log found"
                },
            )

        return build_result(
            "AUTH-LOGS",
            "Authentication Logs",
            "WARNING",
            {
                "details": "Windows Security Event Log not found"
            },
        )

    # LINUX
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