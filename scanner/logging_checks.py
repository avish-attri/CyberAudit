import os


def check_auth_logs():
    """
    Check if authentication logs exist.
    """
    log_path = "/var/log/auth.log"
    if os.path.exists(log_path):
        return {
            "name": "Authentication Logs",
            "status": "PASS",
            "risk": "Low",
            "details": "Authentication logs found",
            "recommendation": "Monitor logs regularly",
        }
    return {
        "name": "Authentication Logs",
        "status": "WARNING",
        "risk": "Medium",
        "details": "Authentication logs not found",
        "recommendation": "Enable system logging",
    }
