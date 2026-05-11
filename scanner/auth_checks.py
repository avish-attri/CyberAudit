from scanner.utils import run_command


def check_uid_zero_users():
    """
    Detect users with UID 0.
    """
    try:
        users = []
        with open("/etc/passwd", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.split(":")
                username = parts[0]
                uid = parts[2]
                if uid == "0":
                    users.append(username)

        if len(users) == 1 and users[0] == "root":
            return {
                "name": "UID 0 Users",
                "status": "PASS",
                "risk": "Low",
                "details": "Only root user has UID 0",
                "recommendation": "No action needed",
            }

        return {
            "name": "UID 0 Users",
            "status": "FAIL",
            "risk": "High",
            "details": f"Multiple UID 0 users found: {', '.join(users)}",
            "recommendation": "Remove unnecessary UID 0 privileges",
        }
    except Exception as e:
        return {
            "name": "UID 0 Users",
            "status": "ERROR",
            "risk": "Unknown",
            "details": str(e),
            "recommendation": "Check file permissions",
        }


def check_ssh_root_login():
    """
    Check if SSH root login is enabled.
    """
    try:
        with open("/etc/ssh/sshd_config", "r", encoding="utf-8") as f:
            data = f.read()

        if "PermitRootLogin no" in data:
            return {
                "name": "SSH Root Login",
                "status": "PASS",
                "risk": "Low",
                "details": "Root login via SSH is disabled",
                "recommendation": "No action needed",
            }

        return {
            "name": "SSH Root Login",
            "status": "FAIL",
            "risk": "High",
            "details": "Root login via SSH may be enabled",
            "recommendation": "Set PermitRootLogin no in sshd_config",
        }
    except Exception as e:
        return {
            "name": "SSH Root Login",
            "status": "ERROR",
            "risk": "Unknown",
            "details": str(e),
            "recommendation": "Check SSH configuration",
        }


def check_ssh_password_auth():
    """
    Check if password authentication is enabled.
    """
    try:
        with open("/etc/ssh/sshd_config", "r", encoding="utf-8") as f:
            data = f.read()

        if "PasswordAuthentication no" in data:
            return {
                "name": "SSH Password Authentication",
                "status": "PASS",
                "risk": "Low",
                "details": "Password authentication disabled",
                "recommendation": "No action needed",
            }

        return {
            "name": "SSH Password Authentication",
            "status": "WARNING",
            "risk": "Medium",
            "details": "Password authentication enabled",
            "recommendation": "Use SSH keys instead of passwords",
        }
    except Exception as e:
        return {
            "name": "SSH Password Authentication",
            "status": "ERROR",
            "risk": "Unknown",
            "details": str(e),
            "recommendation": "Check SSH configuration",
        }
