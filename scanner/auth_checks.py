from pathlib import Path
from scanner.utils import build_result, run_command, format_details, not_available_result
import platform

def check_uid_zero_users():    
    if platform.system() == "Windows":
        return not_available_result(
            "AUTH-UID0-USERS",
            "UID 0 Users",
        )
    
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
            "details": format_details(str(e)),
            "recommendation": "Check file permissions",
        }


def check_ssh_root_login():
    if platform.system() == "Windows":
        return not_available_result(
            "AUTH-SSH-ROOT",
            "SSH Root Login",
        )
    
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
            "details": format_details(str(e)),
            "recommendation": "Check SSH configuration",
        }


def check_ssh_password_auth():
    if platform.system() == "Windows":
        return not_available_result(
            "AUTH-SSH-PASSWORD",
            "SSH Password Authentication",
        )
    
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
            "details": format_details(str(e)),
            "recommendation": "Check SSH configuration",
        }


def check_guest_account():
    if platform.system() == "Windows":

        result = run_command("net user Guest")

        if not result["success"]:

            return build_result(
                "AUTH-GUEST-ACCOUNT",
                "Guest Account Check",
                "UNKNOWN",
                {
                    "error": result.get("error"),
                },
            )

        output = result["output"].lower()

        if (
            "account active" in output
            and "yes" in output
        ):

            return build_result(
                "AUTH-GUEST-ACCOUNT",
                "Guest Account Check",
                "FAIL",
                {
                    "details": "Guest account is enabled",
                },
            )

        return build_result(
            "AUTH-GUEST-ACCOUNT",
            "Guest Account Check",
            "PASS",
            {
                "details": "Guest account is disabled",
            },
        )
    
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

    try:
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
    except Exception as e:
        return build_result(
            "AUTH-GUEST-ACCOUNT",
            "Guest Account Check",
            "unknown",
            {
                "error": str(e),
            },
        )


def check_password_policy():
    if platform.system() == "Windows":

        result = run_command("net accounts")

        if not result["success"]:

            return build_result(
                "AUTH-PASSWORD-POLICY",
                "Password Expiry Policy",
                "UNKNOWN",
                {
                    "error": result.get("error"),
                },
            )

        output = result["output"]

        max_age = None

        for line in output.splitlines():

            if "maximum password age" in line.lower():

                try:
                    max_age = int(
                        "".join(
                            c for c in line
                            if c.isdigit()
                        )
                    )
                except Exception:
                    pass

                break

        status = "PASS"

        if max_age is None:
            status = "UNKNOWN"

        elif max_age > 90:
            status = "WARNING"

        return build_result(
            "AUTH-PASSWORD-POLICY",
            "Password Expiry Policy",
            status,
            {
                "pass_max_days": max_age,
            },
        )
     
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
    try:
        with config.open("r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                cleaned = line.strip()
                if cleaned.startswith("PASS_MAX_DAYS"):
                    parts = cleaned.split()
                    if len(parts) >= 2:
                        try:
                            max_days = int(parts[1])
                        except ValueError:
                            max_days = None
                            break

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
    except Exception as e:
        return build_result(
            "AUTH-PASSWORD-POLICY",
            "Password Expiry Policy",
            "unknown",
            {
                "error": str(e),
            },
        )


def check_empty_password_accounts():

    if platform.system() == "Windows":

        result = run_command(
            "net accounts"
        )

        if not result["success"]:

            return build_result(
                "AUTH-EMPTY-PASSWORDS",
                "Empty Password Accounts",
                "UNKNOWN",
                {
                    "details":
                    "Unable to determine password policy"
                },
            )

        output = result["output"]

        min_length = None

        for line in output.splitlines():

            if "minimum password length" in line.lower():

                try:
                    min_length = int(
                        line.split()[-1]
                    )
                except Exception:
                    pass

                break

        if min_length is None:

            return build_result(
                "AUTH-EMPTY-PASSWORDS",
                "Empty Password Accounts",
                "UNKNOWN",
                {
                    "details":
                    "Unable to determine password policy"
                },
            )

        if min_length == 0:

            return build_result(
                "AUTH-EMPTY-PASSWORDS",
                "Empty Password Accounts",
                "FAIL",
                {
                    "details":
                    "Windows allows empty passwords"
                },
            )

        return build_result(
            "AUTH-EMPTY-PASSWORDS",
            "Empty Password Accounts",
            "PASS",
            {
                "details":
                f"Minimum password length is {min_length}"
            },
        )

    shadow = Path("/etc/shadow")

    if not shadow.exists():
        return build_result(
            "AUTH-EMPTY-PASSWORDS",
            "Empty Password Accounts",
            "UNKNOWN",
            {
                "reason": "/etc/shadow missing",
            },
        )

    try:

        empty_accounts = []

        with shadow.open(
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as file:

            for line in file:

                parts = line.strip().split(":")

                if len(parts) < 2:
                    continue

                username = parts[0]
                password_field = parts[1]

                if password_field == "":
                    empty_accounts.append(username)

        status = "PASS"

        if empty_accounts:
            status = "FAIL"

        return build_result(
            "AUTH-EMPTY-PASSWORDS",
            "Empty Password Accounts",
            status,
            {
                "accounts": empty_accounts,
                "count": len(empty_accounts),
            },
        )

    except Exception as e:

        return build_result(
            "AUTH-EMPTY-PASSWORDS",
            "Empty Password Accounts",
            "UNKNOWN",
            {
                "error": str(e),
            },
        )