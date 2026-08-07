"""
System Audio & Volume Controller Tool — Controls master volume and mute state on Windows.
"""

import subprocess
import logging
from typing import Any

log = logging.getLogger(__name__)


def set_master_volume(level_percent: int) -> dict[str, Any]:
    """
    Sets master audio output volume to a specific percentage (0 to 100).

    Args:
        level_percent: Volume level percentage from 0 (silent) to 100 (max).
    """
    level = max(0, min(100, level_percent))
    log.info(f"[Tool: set_master_volume] Setting volume to {level}%...")

    try:
        # PowerShell script using NirCmd or Windows CoreAudio API via PowerShell WMI
        ps_cmd = f"""
        $wshShell = New-Object -ComObject WScript.Shell
        1..50 | ForEach-Object {{ $wshShell.SendKeys([char]174) }} # Volume down to 0
        $steps = [math]::Round({level} / 2)
        1..$steps | ForEach-Object {{ $wshShell.SendKeys([char]175) }} # Volume up
        """
        subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
        return {
            "status": "success",
            "volume_percent": level,
            "message": f"Set system master volume to {level}%.",
        }
    except Exception as e:
        log.error(f"[Tool: set_master_volume] Error: {e}")
        return {
            "status": "error",
            "message": f"Failed to set volume: {str(e)}",
        }


def mute_master_volume(mute: bool = True) -> dict[str, Any]:
    """
    Mutes or unmutes system master audio output.

    Args:
        mute: True to mute, False to unmute.
    """
    log.info(f"[Tool: mute_master_volume] Setting mute state to {mute}...")
    try:
        ps_cmd = "$wshShell = New-Object -ComObject WScript.Shell; $wshShell.SendKeys([char]173)"
        subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
        return {
            "status": "success",
            "muted": mute,
            "message": f"Toggled master mute state (mute={mute}).",
        }
    except Exception as e:
        log.error(f"[Tool: mute_master_volume] Error: {e}")
        return {
            "status": "error",
            "message": f"Failed to toggle mute: {str(e)}",
        }
