import subprocess


def run_command(command):
    """
    Runs a shell command safely and returns output.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )
        return {
            "success": True,
            "output": result.stdout.strip(),
            "error": result.stderr.strip(),
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e),
        }
