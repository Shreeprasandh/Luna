"""
Remote Mobile Control & Laptop Bridge Tool — Enables controlling your laptop from your mobile phone.
Capabilities:
- Get Mobile Remote Access URL & Local Network IP.
- Execute remote desktop commands (launch VS Code, create folders, play songs, run terminal commands).
"""

import os
import socket
import subprocess
import logging
from typing import Any

log = logging.getLogger(__name__)


def get_mobile_remote_url() -> dict[str, Any]:
    """
    Returns the local network IP address and URL to access Luna's panel from your mobile phone on the same Wi-Fi.
    """
    log.info("[Tool: get_mobile_remote_url] Fetching local IP for mobile access...")
    try:
        # Get primary local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()

        panel_mobile_url = f"http://{local_ip}:3000"
        backend_mobile_url = f"http://{local_ip}:8000"

        return {
            "status": "success",
            "local_ip": local_ip,
            "mobile_panel_url": panel_mobile_url,
            "mobile_backend_url": backend_mobile_url,
            "instructions": f"Open '{panel_mobile_url}' in your mobile browser while connected to the same Wi-Fi.",
        }
    except Exception as e:
        log.error(f"[Tool: get_mobile_remote_url] Error: {e}")
        return {"status": "error", "message": f"Failed to get mobile IP: {str(e)}"}


def execute_remote_laptop_command(action_type: str, target_name: str = "", extra_params: str = "") -> dict[str, Any]:
    """
    Executes a remote laptop command triggered from mobile (e.g. launch VS Code, create folder, play song, open terminal).

    Args:
        action_type: Type of action ('create_project_folder', 'launch_vscode', 'open_terminal', 'play_music').
        target_name: Project folder name or song title.
        extra_params: Optional command parameters.
    """
    act = action_type.strip().lower()
    log.info(f"[Tool: execute_remote_laptop_command] Executing remote action '{act}' for target '{target_name}'...")

    try:
        if act in ("create_project_folder", "create_folder"):
            folder_path = os.path.abspath(target_name or "new_project")
            os.makedirs(folder_path, exist_ok=True)
            # Launch VS Code in that folder
            subprocess.Popen(["cmd", "/c", "code", folder_path], shell=True)
            return {
                "status": "success",
                "action": "create_folder_and_vscode",
                "folder_path": folder_path,
                "message": f"Created folder '{folder_path}' and opened VS Code on your laptop.",
            }

        elif act == "launch_vscode":
            subprocess.Popen(["cmd", "/c", "code", "."], shell=True)
            return {"status": "success", "message": "Opened VS Code on laptop."}

        elif act == "open_terminal":
            subprocess.Popen(["cmd", "/c", "start", "wt"], shell=True)
            return {"status": "success", "message": "Opened Windows Terminal on laptop."}

        elif act == "play_music":
            from tools.media import play_spotify_song
            return play_spotify_song(target_name or "focus music")

        else:
            return {"status": "error", "message": f"Unknown remote action: '{act}'"}

    except Exception as e:
        log.error(f"[Tool: execute_remote_laptop_command] Error: {e}")
        return {"status": "error", "message": f"Remote command failed: {str(e)}"}
