"""
Weather & Forecast Diagnostic Tool — Checks real-time weather, temperature, and conditions.
"""

import httpx
import logging
from typing import Any

log = logging.getLogger(__name__)


def get_weather(city: str = "London") -> dict[str, Any]:
    """
    Fetches real-time weather conditions, temperature, humidity, and wind speed for a specified city.

    Args:
        city: City name (e.g. 'London', 'New York', 'Tokyo', 'Chennai').

    Returns:
        Dict with status, city, temperature, condition, and humidity.
    """
    clean_city = city.strip()
    log.info(f"[Tool: get_weather] Fetching weather for '{clean_city}'...")

    try:
        url = f"https://wttr.in/{clean_city}?format=j1"
        res = httpx.get(url, timeout=5.0)

        if res.status_code == 200:
            data = res.json()
            curr = data["current_condition"][0]
            area = data["nearest_area"][0]["areaName"][0]["value"]
            country = data["nearest_area"][0]["country"][0]["value"]

            return {
                "status": "success",
                "city": f"{area}, {country}",
                "temperature_celsius": float(curr["temp_C"]),
                "feels_like_celsius": float(curr["FeelsLikeC"]),
                "condition": curr["weatherDesc"][0]["value"],
                "humidity_percent": int(curr["humidity"]),
                "wind_speed_kmh": int(curr["windspeedKmph"]),
            }
        else:
            return {"status": "error", "message": f"Weather API returned status code {res.status_code}"}
    except Exception as e:
        log.error(f"[Tool: get_weather] Error fetching weather for '{city}': {e}")
        return {
            "status": "error",
            "message": f"Failed to fetch weather: {str(e)}",
        }
