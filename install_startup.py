"""
Windows Startup Installer for Luna.
Adds Luna to Windows Startup folder so it boots automatically when laptop turns on.
"""

import os
import sys
import logging

log = logging.getLogger(__name__)


def install_to_startup():
    startup_dir = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
    vbs_path = os.path.join(startup_dir, "LunaStartup.vbs")

    repo_dir = os.path.abspath(os.path.dirname(__file__))
    bat_path = os.path.join(repo_dir, "Luna.bat")

    vbs_content = f'Set WshShell = CreateObject("WScript.Shell")\nWshShell.Run """{bat_path}""", 0, False\n'

    try:
        with open(vbs_path, "w", encoding="utf-8") as f:
            f.write(vbs_content)
        print(f"[SUCCESS] Luna registered to Windows Startup!")
        print(f"Startup Script: '{vbs_path}'")
        print("Luna will now start automatically whenever your laptop turns on, Sir!")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to register startup script: {e}")
        return False


if __name__ == "__main__":
    install_to_startup()
