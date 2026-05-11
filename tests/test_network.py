from scanner.network_checks import (
    check_open_ports,
    check_firewall_status,
)


def test_check_open_ports():
    result = check_open_ports()
    assert isinstance(result, dict)
    assert "status" in result


def test_check_firewall_status():
    result = check_firewall_status()
    assert isinstance(result, dict)
    assert "status" in result
