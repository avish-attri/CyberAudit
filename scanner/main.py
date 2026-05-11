from scanner.auth_checks import (
    check_uid_zero_users,
    check_ssh_root_login,
    check_ssh_password_auth,
)
from scanner.network_checks import (
    check_open_ports,
    check_firewall_status,
)
from scanner.file_checks import (
    check_passwd_permissions,
    check_shadow_permissions,
    check_world_writable_files,
)
from scanner.system_checks import (
    check_kernel_version,
    check_pending_updates,
)
from scanner.logging_checks import check_auth_logs
from scanner.scorer import calculate_score


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
    results.append(check_kernel_version())
    results.append(check_pending_updates())
    results.append(check_auth_logs())
    return results


def build_scan_report():
    results = run_all_checks()
    score = calculate_score(results)
    return {
        "score": score,
        "results": results,
    }
