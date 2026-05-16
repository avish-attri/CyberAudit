import socket
import time

from scanner.auth_checks import (
    check_uid_zero_users,
    check_ssh_root_login,
    check_ssh_password_auth,
    check_guest_account,
    check_password_policy,
    check_empty_password_accounts,
)
from scanner.network_checks import (
    check_open_ports,
    check_firewall_status,
)
from scanner.file_checks import (
    check_passwd_permissions,
    check_shadow_permissions,
    check_world_writable_files,
    check_suid_binaries,
)
from scanner.system_checks import (
    check_kernel_version,
    check_pending_updates,
    check_disk_usage,
    check_security_updates,
)
from scanner.logging_checks import check_auth_logs
from scanner.log_checks import check_failed_logins
from scanner.service_checks import (
    check_ssh_service,
    check_running_services,
)
from scanner.scorer import calculate_score


def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def run_all_checks():
    results = []
    results.append(check_uid_zero_users())
    results.append(check_ssh_root_login())
    results.append(check_ssh_password_auth())
    results.append(check_open_ports())
    results.append(check_firewall_status())
    results.append(check_passwd_permissions())
    results.append(check_shadow_permissions())
    results.append(check_world_writable_files())
    results.append(check_suid_binaries())
    results.append(check_kernel_version())
    results.append(check_pending_updates())
    results.append(check_disk_usage())
    results.append(check_security_updates())
    results.append(check_failed_logins())
    results.append(check_ssh_service())
    results.append(check_running_services())
    results.append(check_guest_account())
    results.append(check_password_policy())
    results.append(check_empty_password_accounts())
    results.append(check_auth_logs())
    return results


def build_scan_report():
    start_time = time.perf_counter()
    results = run_all_checks()
    duration_seconds = time.perf_counter() - start_time
    score = calculate_score(results)
    return {
        "score": score,
        "results": results,
        "host_ip": get_local_ip(),
        "duration_seconds": round(duration_seconds, 2),
    }
