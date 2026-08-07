"""
Application & Desktop Launcher Tool — Allows Luna to open desktop apps and browser URLs.
"""

import os
import subprocess
import webbrowser
import logging
from typing import Any

log = logging.getLogger(__name__)

# Common app mapping for Windows
APP_MAP = {
    "code": "code",
    "vscode": "code",
    "chrome": "chrome",
    "browser": "chrome",
    "notepad": "notepad",
    "calculator": "calc",
    "calc": "calc",
    "cmd": "cmd",
    "terminal": "wt",
    "powershell": "powershell",
    "spotify": "spotify",
    "explorer": "explorer",
}


def launch_app(app_name: str) -> dict[str, Any]:
    """
    Launches a desktop application by name (e.g. 'code', 'chrome', 'notepad', 'calculator', 'spotify').

    Args:
        app_name: Name of the application to launch.

    Returns:
        Dict with status and app name.
    """
    clean_name = app_name.strip().lower()
    target_executable = APP_MAP.get(clean_name, clean_name)

    log.info(f"[Tool: launch_app] Launching application '{target_executable}'...")
    try:
        if os.name == "nt":
            subprocess.Popen(["cmd", "/c", "start", "", target_executable], shell=True)
        else:
            subprocess.Popen([target_executable])

        return {
            "status": "success",
            "app_name": app_name,
            "message": f"Successfully launched {app_name}.",
        }
    except Exception as e:
        log.error(f"[Tool: launch_app] Error launching '{app_name}': {e}")
        return {
            "status": "error",
            "message": f"Failed to launch '{app_name}': {str(e)}",
        }


def open_url_in_browser(url: str) -> dict[str, Any]:
    """
    Opens a website URL in the user's default desktop browser.

    Args:
        url: The web URL to open (e.g. 'https://github.com').
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    log.info(f"[Tool: open_url_in_browser] Opening URL '{url}'...")
    try:
        webbrowser.open(url)
        return {
            "status": "success",
            "url": url,
            "message": f"Opened {url} in default browser.",
        }
    except Exception as e:
        log.error(f"[Tool: open_url_in_browser] Error: {e}")
        return {
            "status": "error",
            "message": f"Failed to open URL: {str(e)}",
        }
