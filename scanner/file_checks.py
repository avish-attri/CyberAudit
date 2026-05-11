import os
from scanner.utils import run_command


def check_passwd_permissions():
    """
    Check permissions of /etc/passwd.
    """
    try:
        permissions = oct(os.stat("/etc/passwd").st_mode)[-3:]
        if permissions == "644":
            return {
                "name": "/etc/passwd Permissions",
                "status": "PASS",
                "risk": "Low",
                "details": "Permissions correctly set to 644",
                "recommendation": "No action needed",
            }
        return {
            "name": "/etc/passwd Permissions",
            "status": "WARNING",
            "risk": "Medium",
            "details": f"Permissions are {permissions}",
            "recommendation": "Set permissions to 644",
        }
    except Exception as e:
        return {
            "name": "/etc/passwd Permissions",
            "status": "ERROR",
            "risk": "Unknown",
            "details": str(e),
            "recommendation": "Check file permissions",
        }


def check_shadow_permissions():
    """
    Check permissions of /etc/shadow.
    """
    try:
        permissions = oct(os.stat("/etc/shadow").st_mode)[-3:]
        if permissions == "640":
            return {
                "name": "/etc/shadow Permissions",
                "status": "PASS",
                "risk": "Low",
                "details": "Permissions correctly set to 640",
                "recommendation": "No action needed",
            }
        return {
            "name": "/etc/shadow Permissions",
            "status": "FAIL",
            "risk": "High",
            "details": f"Permissions are {permissions}",
            "recommendation": "Restrict access to /etc/shadow",
        }
    except Exception as e:
        return {
            "name": "/etc/shadow Permissions",
            "status": "ERROR",
            "risk": "Unknown",
            "details": str(e),
            "recommendation": "Run with proper permissions",
        }


def check_world_writable_files():
    """
    Find world-writable files inside /home.
    """
    command = "find /home -type f -perm -0002 2>/dev/null | head"
    result = run_command(command)
    if not result["success"]:
        return {
            "name": "World Writable Files",
            "status": "ERROR",
            "risk": "Unknown",
            "details": result["error"],
            "recommendation": "Check find command",
        }

    files = result["output"].split("\n") if result["output"] else []
    if len(files) == 0:
        return {
            "name": "World Writable Files",
            "status": "PASS",
            "risk": "Low",
            "details": "No world writable files found",
            "recommendation": "No action needed",
        }
    return {
        "name": "World Writable Files",
        "status": "WARNING",
        "risk": "Medium",
        "details": f"Found {len(files)} writable files",
        "recommendation": "Restrict write permissions",
    }
