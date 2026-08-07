"""
YouTube Video Search & Playback Controller Tool — Searches YouTube and controls media playback.
"""

import urllib.parse
import webbrowser
import subprocess
import logging
from typing import Any

log = logging.getLogger(__name__)


def play_youtube_video(query: str) -> dict[str, Any]:
    """
    Searches YouTube for a query and opens the video or search results directly.

    Args:
        query: Video title or topic to play on YouTube.
    """
    clean_query = query.strip()
    encoded = urllib.parse.quote(clean_query)
    yt_url = f"https://www.youtube.com/results?search_query={encoded}"

    log.info(f"[Tool: play_youtube_video] Playing YouTube video for '{clean_query}'...")
    try:
        webbrowser.open(yt_url)
        return {
            "status": "success",
            "query": clean_query,
            "url": yt_url,
            "message": f"Opened YouTube player for '{clean_query}'.",
        }
    except Exception as e:
        log.error(f"[Tool: play_youtube_video] Error: {e}")
        return {"status": "error", "message": f"Failed to play YouTube video: {str(e)}"}


def control_youtube_player(action: str = "play_pause") -> dict[str, Any]:
    """
    Controls desktop video playback (play, pause, toggle captions, fullscreen).

    Args:
        action: Action type: 'play_pause', 'mute', 'fullscreen', 'toggle_captions'.
    """
    act = action.strip().lower()
    log.info(f"[Tool: control_youtube_player] Executing media action '{act}'...")

    try:
        # Key mapping for YouTube web player
        key_code = "k"  # Default 'k' toggles play/pause in YouTube
        if act == "mute":
            key_code = "m"
        elif act == "fullscreen":
            key_code = "f"
        elif act == "toggle_captions":
            key_code = "c"

        ps_cmd = f"$wshShell = New-Object -ComObject WScript.Shell; $wshShell.SendKeys('{key_code}')"
        subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)

        return {
            "status": "success",
            "action": act,
            "message": f"Executed YouTube playback control '{act}'.",
        }
    except Exception as e:
        log.error(f"[Tool: control_youtube_player] Error: {e}")
        return {"status": "error", "message": f"Playback control failed: {str(e)}"}
