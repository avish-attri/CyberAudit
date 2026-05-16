from unittest.mock import patch, MagicMock

from scanner.utils import build_result, run_command


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


def test_build_result_formats_disk_usage_data():
    result = build_result(
        "SYSTEM-DISK-USAGE",
        "Root Disk Usage",
        "warn",
        {"used_percent": 60.29, "free_gb": 188.73},
    )

    assert result["details"] == "60.29% used, 188.73 GB free"
    assert result["status"] == "WARNING"
    assert result["risk"] == "Medium"
