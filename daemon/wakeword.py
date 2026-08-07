"""
Luna Hands-Free Wake-Word Listener Engine.
Continuously listens for wake phrase ("Hey Luna" / "Luna") and triggers voice turn.
"""

import os
import time
import logging
from typing import Callable

log = logging.getLogger(__name__)

# Wake phrases supported
WAKE_WORDS = ["hey luna", "luna", "hi luna", "ok luna", "okay luna"]


def is_wake_word_detected(transcript: str) -> bool:
    """
    Checks if any wake word phrase is present in the recognized audio transcript.
    """
    clean_text = transcript.strip().lower()
    return any(phrase in clean_text for phrase in WAKE_WORDS)


def start_wakeword_listener(on_wake_callback: Callable[[], None], poll_interval: float = 0.5) -> None:
    """
    Starts a background listener for the wake word.
    When detected, invokes on_wake_callback.
    """
    log.info("Starting Luna Hands-Free Wake-Word Listener ('Hey Luna')...")
    import speech_recognition as sr

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1.0)
        log.info("Wake-Word Listener active. Say 'Hey Luna' anytime, Sir.")

        while True:
            try:
                audio = recognizer.listen(source, timeout=3.0, phrase_time_limit=4.0)
                text = recognizer.recognize_google(audio).lower()
                log.debug(f"[WakeWord Audio] Heard: '{text}'")

                if is_wake_word_detected(text):
                    log.info(f"WAKE WORD DETECTED: '{text}' -> Triggering Luna!")
                    on_wake_callback()

            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except Exception as e:
                log.warning(f"WakeWord listener cycle exception: {e}")
                time.sleep(poll_interval)
