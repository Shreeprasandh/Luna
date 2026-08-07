"""
System Power & Battery Inspector Tool — Inspects laptop battery status, power source, and estimated time remaining.
"""

import logging
from typing import Any
import psutil

log = logging.getLogger(__name__)


def get_power_status() -> dict[str, Any]:
    """
    Inspects battery percentage, charging state, and estimated time remaining.
    """
    log.info("[Tool: get_power_status] Checking battery and power status...")
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return {
                "status": "success",
                "is_desktop": True,
                "message": "Desktop PC plugged into AC power (no battery).",
            }

        percent = round(battery.percent, 1)
        plugged = battery.power_plugged
        secs_left = battery.secsleft

        if secs_left == psutil.POWER_TIME_UNLIMITED:
            time_str = "Plugged into AC power (Fully charged / Charging)"
        elif secs_left == psutil.POWER_TIME_UNKNOWN:
            time_str = "Calculating time remaining..."
        else:
            mins = int(secs_left / 60)
            hrs = mins // 60
            rem_mins = mins % 60
            time_str = f"{hrs}h {rem_mins}m remaining" if hrs > 0 else f"{mins}m remaining"

        return {
            "status": "success",
            "is_desktop": False,
            "battery_percent": percent,
            "is_charging": plugged,
            "time_remaining": time_str,
            "message": f"Battery at {percent}% ({'Charging' if plugged else time_str}).",
        }
    except Exception as e:
        log.error(f"[Tool: get_power_status] Error: {e}")
        return {"status": "error", "message": f"Battery inspection failed: {str(e)}"}
