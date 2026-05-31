import os
import platform
import subprocess

from scanner.utils import (
    build_result,
    run_command,
    not_available_result,
    format_details,
)

def check_passwd_permissions():
    # WINDOWS
    if platform.system() == "Windows":

        return not_available_result(
            "FILE-PASSWD-PERMISSIONS",
            "/etc/passwd Permissions",
        )

    # LINUX
    try:

        permissions = oct(
            os.stat("/etc/passwd").st_mode
        )[-3:]

        if permissions == "644":

            return build_result(
                "FILE-PASSWD-PERMISSIONS",
                "/etc/passwd Permissions",
                "PASS",
                {
                    "details":
                    "Permissions correctly set to 644"
                },
            )

        return build_result(
            "FILE-PASSWD-PERMISSIONS",
            "/etc/passwd Permissions",
            "WARNING",
            {
                "details":
                f"Permissions are {permissions}"
            },
        )

    except Exception as e:

        return build_result(
            "FILE-PASSWD-PERMISSIONS",
            "/etc/passwd Permissions",
            "ERROR",
            {
                "error": str(e)
            },
        )


def check_shadow_permissions():
    # WINDOWS
    if platform.system() == "Windows":

        return not_available_result(
            "FILE-SHADOW-PERMISSIONS",
            "/etc/shadow Permissions",
        )

    # LINUX
    try:

        permissions = oct(
            os.stat("/etc/shadow").st_mode
        )[-3:]

        if permissions == "640":

            return build_result(
                "FILE-SHADOW-PERMISSIONS",
                "/etc/shadow Permissions",
                "PASS",
                {
                    "details":
                    "Permissions correctly set to 640"
                },
            )

        return build_result(
            "FILE-SHADOW-PERMISSIONS",
            "/etc/shadow Permissions",
            "FAIL",
            {
                "details":
                f"Permissions are {permissions}"
            },
        )

    except Exception as e:

        return build_result(
            "FILE-SHADOW-PERMISSIONS",
            "/etc/shadow Permissions",
            "ERROR",
            {
                "error": str(e)
            },
        )


def check_world_writable_files():
    # WINDOWS
    if platform.system() == "Windows":

        result = run_command(
            "icacls C:\\Users"
        )

        if not result["success"]:

            return build_result(
                "FILE-WORLD-WRITABLE",
                "World Writable Files",
                "UNKNOWN",
                {
                    "details":
                    "Unable to audit Windows file permissions"
                },
            )

        output = result["output"]

        writable_entries = 0

        for line in output.splitlines():

            if (
                "Everyone:(F)" in line
                or "Everyone:(M)" in line
            ):
                writable_entries += 1

        if writable_entries == 0:

            return build_result(
                "FILE-WORLD-WRITABLE",
                "World Writable Files",
                "PASS",
                {
                    "details":
                    "No potentially world-writable files found"
                },
            )

        return build_result(
            "FILE-WORLD-WRITABLE",
            "World Writable Files",
            "WARNING",
            {
                "details":
                f"Found {writable_entries} potentially world-writable entries"
            },
        )

    # LINUX
    command = (
        "find /home -type f "
        "-perm -0002 2>/dev/null | head"
    )

    result = run_command(command)

    if not result["success"]:

        return build_result(
            "FILE-WORLD-WRITABLE",
            "World Writable Files",
            "ERROR",
            {
                "error":
                result.get("error")
            },
        )

    files = (
        result["output"].split("\n")
        if result["output"]
        else []
    )

    if len(files) == 0:

        return build_result(
            "FILE-WORLD-WRITABLE",
            "World Writable Files",
            "PASS",
            {
                "details":
                "No world writable files found"
            },
        )

    return build_result(
        "FILE-WORLD-WRITABLE",
        "World Writable Files",
        "WARNING",
        {
            "details":
            f"Found {len(files)} writable files"
        },
    )

def check_suid_binaries():
    # WINDOWS
    if platform.system() == "Windows":
        return not_available_result(
            "FILE-SUID-BINARIES",
            "SUID Binary Check",
        )


    # LINUX
    try:

        result = subprocess.run(
            "find / -perm -4000 -type f "
            "2>/dev/null | head -50",
            shell=True,
            capture_output=True,
            text=True,
        )

        binaries = (
            result.stdout.splitlines()
        )

        count = len(binaries)

        status = "PASS"

        if count > 40:
            status = "WARNING"

        return build_result(
            "FILE-SUID-BINARIES",
            "SUID Binary Check",
            status,
            {
                "count": count,
                "sample":
                binaries[:10],
            },
        )

    except Exception as e:

        return build_result(
            "FILE-SUID-BINARIES",
            "SUID Binary Check",
            "ERROR",
            {
                "error": str(e),
            },
        )