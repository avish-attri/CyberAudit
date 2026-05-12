from pathlib import Path

from scanner.utils import build_result, run_command


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


def check_guest_account():
    passwd_path = Path("/etc/passwd")

    if not passwd_path.exists():
        return build_result(
            "AUTH-GUEST-ACCOUNT",
            "Guest Account Check",
            "unknown",
            {
                "reason": "/etc/passwd missing",
            },
        )

    found = False
    with passwd_path.open("r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            if "guest" in line.lower():
                found = True
                break

    status = "fail" if found else "pass"
    return build_result(
        "AUTH-GUEST-ACCOUNT",
        "Guest Account Check",
        status,
        {
            "guest_account_found": found,
        },
    )


def check_password_policy():
    config = Path("/etc/login.defs")

    if not config.exists():
        return build_result(
            "AUTH-PASSWORD-POLICY",
            "Password Expiry Policy",
            "unknown",
            {
                "reason": "login.defs missing",
            },
        )

    max_days = None
    with config.open("r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            cleaned = line.strip()
            if cleaned.startswith("PASS_MAX_DAYS"):
                parts = cleaned.split()
                if len(parts) >= 2:
                    max_days = int(parts[1])

    status = "pass"
    if max_days is None:
        status = "unknown"
    elif max_days > 90:
        status = "warn"

    return build_result(
        "AUTH-PASSWORD-POLICY",
        "Password Expiry Policy",
        status,
        {
            "pass_max_days": max_days,
        },
    )


def check_empty_password_accounts():
    shadow = Path("/etc/shadow")

    if not shadow.exists():
        return build_result(
            "AUTH-EMPTY-PASSWORDS",
            "Empty Password Accounts",
            "unknown",
            {
                "reason": "/etc/shadow missing",
            },
        )

    empty_accounts = []
    with shadow.open("r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) < 2:
                continue

            username = parts[0]
            password_field = parts[1]
            if password_field == "":
                empty_accounts.append(username)

    status = "pass"
    if empty_accounts:
        status = "fail"

    return build_result(
        "AUTH-EMPTY-PASSWORDS",
        "Empty Password Accounts",
        status,
        {
            "accounts": empty_accounts,
            "count": len(empty_accounts),
        },
    )
