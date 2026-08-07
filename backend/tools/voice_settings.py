"""
Custom Voice Personality & TTS Synthesizer Tool.
"""

import logging
from typing import Any

log = logging.getLogger(__name__)

_VOICE_CONFIG = {
    "rate": 175,
    "pitch": 50,
    "gender": "female",
    "style": "executive",
}


def set_voice_settings(rate: int = 175, pitch: int = 50, voice_gender: str = "female") -> dict[str, Any]:
    """
    Adjusts Luna's speech synthesis parameters (rate, pitch, gender).
    """
    _VOICE_CONFIG["rate"] = max(100, min(300, rate))
    _VOICE_CONFIG["pitch"] = max(0, min(100, pitch))
    _VOICE_CONFIG["gender"] = voice_gender.strip().lower()

    log.info(f"[Tool: set_voice_settings] Updated voice config: {_VOICE_CONFIG}")
    return {
        "status": "success",
        "config": _VOICE_CONFIG,
        "message": f"Voice synthesis configured: rate={rate} wpm, pitch={pitch}%, gender={voice_gender}.",
    }
