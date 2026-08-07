"""
Daily Focus Shield & Website Blocker Tool.
"""

import logging
from typing import Any

log = logging.getLogger(__name__)

_FOCUS_MODE = {"active": False, "duration_minutes": 25}


def toggle_focus_shield(enable: bool = True, duration_minutes: int = 25) -> dict[str, Any]:
    """
    Enables or disables Pomodoro Daily Focus Shield to block online distractions.
    """
    _FOCUS_MODE["active"] = enable
    _FOCUS_MODE["duration_minutes"] = duration_minutes

    status_str = "ENABLED" if enable else "DISABLED"
    log.info(f"[Tool: toggle_focus_shield] Focus shield {status_str} for {duration_minutes} mins.")

    return {
        "status": "success",
        "focus_active": enable,
        "duration_minutes": duration_minutes,
        "message": f"Daily Focus Shield {status_str} for {duration_minutes} minutes.",
    }
