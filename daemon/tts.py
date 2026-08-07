"""
Text-to-Speech (TTS) Engine — Local offline speech synthesis using pyttsx3.
Zero API cost, zero cloud latency.
"""

import logging
import threading
import pyttsx3

log = logging.getLogger(__name__)

_engine = None
_lock = threading.Lock()


def _get_engine():
    global _engine
    if _engine is None:
        log.info("Initializing pyttsx3 TTS engine...")
        _engine = pyttsx3.init()
        # Set speech rate and volume
        _engine.setProperty("rate", 175)    # Natural reading speed
        _engine.setProperty("volume", 0.9)  # Clear volume level
        
        # Select clear voice if available
        voices = _engine.getProperty("voices")
        if voices:
            # Prefer female/neutral voice if present (e.g. Zira on Windows)
            for v in voices:
                if "zira" in v.name.lower() or "hazel" in v.name.lower():
                    _engine.setProperty("voice", v.id)
                    break
        log.info("TTS Engine initialized.")
    return _engine


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
