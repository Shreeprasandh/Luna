"""
Autonomous Daily Briefing Generator Tool — Synthesizes Weather, Hardware, Git, and Power metrics into an executive 3-point status report.
"""

import logging
from typing import Any
from tools.weather import get_weather
from tools.system import get_system_health
from tools.power import get_power_status
from tools.git_agent import git_status

log = logging.getLogger(__name__)


def generate_morning_briefing(city: str = "London") -> dict[str, Any]:
    """
    Generates a 3-point executive briefing combining Weather, System Health, Battery Power, and Git Status.

    Args:
        city: City for weather report (default 'London').
    """
    log.info("[Tool: generate_morning_briefing] Generating executive briefing...")

    try:
        w = get_weather(city)
        h = get_system_health()
        p = get_power_status()
        g = git_status()

        weather_str = f"{w.get('temperature_celsius')}°C, {w.get('condition')}" if w.get("status") == "success" else "Weather unavailable"
        ram_percent = h.get("ram", {}).get("usage_percent", 0) if h.get("status") == "success" else 0
        power_str = p.get("message", "Power status clear") if p.get("status") == "success" else "AC Power"
        branch_str = g.get("branch", "main") if g.get("status") == "success" else "main"

        points = [
            f"Weather in {city}: {weather_str}.",
            f"System Health: RAM at {ram_percent}%, {power_str}.",
            f"Workspace: On Git branch '{branch_str}' with {g.get('modified_files_count', 0)} modified files.",
        ]

        return {
            "status": "success",
            "executive_summary_points": points,
            "message": "Executive briefing generated successfully.",
        }
    except Exception as e:
        log.error(f"[Tool: generate_morning_briefing] Error: {e}")
        return {"status": "error", "message": f"Briefing generation failed: {str(e)}"}
