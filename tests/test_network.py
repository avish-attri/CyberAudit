from unittest.mock import patch

from scanner.network_checks import (
    check_open_ports,
    check_firewall_status,
)


def test_check_open_ports():
    result = check_open_ports()
    assert isinstance(result, dict)
    assert "status" in result


def test_check_firewall_status_permission_required():
    ufw_failure = {"success": False, "output": "", "error": "Permission denied"}
    firewalld_failure = {"success": False, "output": "", "error": "Command not found"}

    with patch("scanner.network_checks.run_command", side_effect=[ufw_failure, firewalld_failure]):
        result = check_firewall_status()

    assert isinstance(result, dict)
    assert result["status"] == "PERMISSION REQUIRED"
    assert "root/sudo permissions" in result["details"]
