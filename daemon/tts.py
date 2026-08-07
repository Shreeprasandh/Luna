"""
Text-to-Speech (TTS) Engine — Local offline speech synthesis with multi-voice selection.
Supports switching between Female, Male, System voices, and adjustable speech rates.
"""

import logging
import threading
import pyttsx3
from typing import Any

log = logging.getLogger(__name__)

_engine = None
_lock = threading.Lock()
_current_voice_id = None
_speech_rate = 175


def _get_engine():
    global _engine, _current_voice_id, _speech_rate
    if _engine is None:
        log.info("Initializing pyttsx3 TTS engine...")
        _engine = pyttsx3.init()
        _engine.setProperty("rate", _speech_rate)
        _engine.setProperty("volume", 0.95)

        voices = _engine.getProperty("voices")
        if voices:
            # Default to Zira (Female/Neutral) if available
            for v in voices:
                if any(k in v.name.lower() for k in ("zira", "hazel", "eva", "female")):
                    _engine.setProperty("voice", v.id)
                    _current_voice_id = v.id
                    break
            if not _current_voice_id:
                _engine.setProperty("voice", voices[0].id)
                _current_voice_id = voices[0].id

        log.info("TTS Engine initialized.")
    return _engine


def get_available_voices() -> list[dict[str, Any]]:
    """
    Returns a list of all installed system TTS voices available for selection.
    """
    engine = _get_engine()
    voices = engine.getProperty("voices")
    result = []
    for idx, v in enumerate(voices):
        result.append({
            "index": idx,
            "id": v.id,
            "name": v.name,
            "languages": getattr(v, "languages", []),
        })
    return result


def set_voice(voice_index_or_keyword: str | int) -> bool:
    """
    Dynamically switches the active voice engine by index or keyword (e.g. 'zira', 'david', 0, 1).
    """
    global _current_voice_id
    engine = _get_engine()
    voices = engine.getProperty("voices")

    target_id = None

    if isinstance(voice_index_or_keyword, int) and 0 <= voice_index_or_keyword < len(voices):
        target_id = voices[voice_index_or_keyword].id
    elif isinstance(voice_index_or_keyword, str):
        kw = voice_index_or_keyword.lower()
        for v in voices:
            if kw in v.name.lower() or kw in v.id.lower():
                target_id = v.id
                break

    if target_id:
        engine.setProperty("voice", target_id)
        _current_voice_id = target_id
        log.info(f"TTS Voice switched to: {target_id}")
        return True
    return False


def set_speech_rate(rate: int = 175) -> None:
    """
    Adjusts the spoken speech rate (words per minute).
    """
    global _speech_rate
    _speech_rate = rate
    engine = _get_engine()
    engine.setProperty("rate", rate)
    log.info(f"TTS Speech rate set to: {rate}")


def speak(text: str) -> None:
    """
    Speaks the given text out loud asynchronously without blocking execution.

    Args:
        text: Plain text to synthesize and play through speakers.
    """
    if not text or not text.strip():
        return

    def _run():
        with _lock:
            try:
                engine = _get_engine()
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                log.error(f"TTS Speech Error: {e}")

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
