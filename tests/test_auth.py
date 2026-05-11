from scanner.auth_checks import (
    check_uid_zero_users,
    check_ssh_root_login,
    check_ssh_password_auth,
)


def test_check_uid_zero_users():
    result = check_uid_zero_users()
    assert isinstance(result, dict)
    assert "status" in result


def test_check_ssh_root_login():
    result = check_ssh_root_login()
    assert isinstance(result, dict)
    assert "status" in result


def test_check_ssh_password_auth():
    result = check_ssh_password_auth()
    assert isinstance(result, dict)
    assert "status" in result
