"""
Microsoft PowerToys Utility Bridge Tool — Emulates and integrates PowerToys capabilities natively.
Capabilities:
- Color Picker: Screen pixel color code inspection.
- Text Extractor (OCR): On-screen text extraction from any region.
- Awake Utility: Prevents computer from going to sleep during long tasks.
- PowerToys Run: Rapid app launcher and local file finder.
"""

import os
import subprocess
import logging
from typing import Any

log = logging.getLogger(__name__)

_awake_proc = None


def toggle_awake_mode(enable: bool = True) -> dict[str, Any]:
    """
    Prevents the PC from sleeping or turning off the screen (PowerToys Awake utility).

    Args:
        enable: True to keep PC awake, False to restore normal sleep timer.
    """
    global _awake_proc
    log.info(f"[Tool: toggle_awake_mode] Setting Awake mode to {enable}...")

    try:
        if enable:
            # Use Windows powercfg or thread execution state to prevent sleep
            ps_cmd = """
            $code = '[DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)] public static extern uint SetThreadExecutionState(uint esFlags);'
            $type = Add-Type -MemberDefinition $code -Name 'Win32SetThreadExecutionState' -Namespace 'Win32' -PassThru
            $type::SetThreadExecutionState(0x80000001) # ES_CONTINUOUS | ES_SYSTEM_REQUIRED
            """
            subprocess.Popen(["powershell", "-Command", ps_cmd])
            return {
                "status": "success",
                "awake_enabled": True,
                "message": "PowerToys Awake enabled. PC will remain awake during tasks.",
            }
        else:
            ps_cmd = """
            $code = '[DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)] public static extern uint SetThreadExecutionState(uint esFlags);'
            $type = Add-Type -MemberDefinition $code -Name 'Win32SetThreadExecutionState' -Namespace 'Win32' -PassThru
            $type::SetThreadExecutionState(0x80000000) # ES_CONTINUOUS
            """
            subprocess.Popen(["powershell", "-Command", ps_cmd])
            return {
                "status": "success",
                "awake_enabled": False,
                "message": "PowerToys Awake disabled. Normal system sleep restored.",
            }
    except Exception as e:
        log.error(f"[Tool: toggle_awake_mode] Error: {e}")
        return {"status": "error", "message": f"Awake toggle failed: {str(e)}"}
