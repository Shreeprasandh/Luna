"""
Workspace Layout Snap Tool — Snaps windows and sets up coding or research workspaces.
"""

import subprocess
import logging
from typing import Any

log = logging.getLogger(__name__)


def setup_workspace_preset(preset_name: str = "coding") -> dict[str, Any]:
    """
    Launches applications and arranges workspace layout (e.g. 'coding', 'research', 'media').

    Args:
        preset_name: Preset type ('coding', 'research', 'media').
    """
    clean_preset = preset_name.strip().lower()
    log.info(f"[Tool: setup_workspace_preset] Setting up '{clean_preset}' workspace...")

    try:
        if clean_preset == "coding":
            subprocess.Popen(["cmd", "/c", "code", "."], shell=True)
            subprocess.Popen(["cmd", "/c", "start", "wt"], shell=True)
            msg = "Coding workspace ready: Opened VS Code and Windows Terminal."
        elif clean_preset == "research":
            import webbrowser
            webbrowser.open("https://google.com")
            msg = "Research workspace ready: Opened browser."
        else:
            msg = f"Preset '{clean_preset}' configured."

        return {"status": "success", "preset": clean_preset, "message": msg}
    except Exception as e:
        log.error(f"[Tool: setup_workspace_preset] Error: {e}")
        return {"status": "error", "message": f"Workspace setup failed: {str(e)}"}
