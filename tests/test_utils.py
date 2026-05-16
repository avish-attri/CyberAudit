from unittest.mock import patch, MagicMock

from scanner.utils import run_command


def test_run_command_returns_output_and_error():
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = ""
    mock_result.stderr = "command not found"

    with patch("scanner.utils.subprocess.run", return_value=mock_result):
        result = run_command("fakecmd")

    assert result["success"] is False
    assert result["output"] == ""
    assert result["error"] == "command not found"
