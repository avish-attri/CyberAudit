from unittest.mock import patch, MagicMock

from scanner.utils import run_command


def test_run_command_returns_error_output():
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = ""
    mock_result.stderr = "bash: /usr/bin/ufw: Permission denied"

    with patch("scanner.utils.subprocess.run", return_value=mock_result):
        result = run_command("ufw status")

    assert result["success"] is False
    assert result["output"] == ""
    assert "Permission denied" in result["error"]
