"""
Luna Desktop Daemon — Main entry point.

Runs 24/7 in the background on your machine.
Lifecycle:
  IDLE   → Listens for wake word (0% token cost, local CPU)
  ACTIVE → Records voice input, transcribes via local Whisper, queries backend API
  SPEAK  → Synthesizes spoken response via pyttsx3, returns to IDLE
"""

import sys
import time
import logging
import httpx

from tts import speak
from stt import record_audio, transcribe_audio
from wakeword import listen_for_wakeword

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] Daemon: %(message)s",
)
log = logging.getLogger("LunaDaemon")

BACKEND_URL = "http://localhost:8000"


def check_backend_health() -> bool:
    """Checks if the FastAPI backend server is running."""
    try:
        r = httpx.get(f"{BACKEND_URL}/health", timeout=3.0)
        return r.status_code == 200 and r.json().get("status") == "ok"
    except Exception:
        return False


def run_daemon_loop():
    """Main loop for the 24/7 desktop voice assistant."""
    log.info("==========================================")
    log.info("     Luna Desktop Daemon Starting...      ")
    log.info("==========================================")

    # 1. Ensure backend server is reachable
    if not check_backend_health():
        log.warning("Backend API (http://localhost:8000) not responding.")
        log.info("Please start the backend server: uvicorn main:app --port 8000")
        speak("Sir, backend server is offline. Please start the server.")
        return

    # 2. Start session with backend
    session_id = None
    try:
        r = httpx.post(f"{BACKEND_URL}/session/start", timeout=5.0)
        session_id = r.json().get("session_id")
        log.info(f"Connected to backend. Session ID: {session_id}")
    except Exception as e:
        log.error(f"Failed to start backend session: {e}")
        return

    speak("Luna desktop daemon active, Sir.")

    # 3. Main voice assistant loop
    try:
        while True:
            # ── IDLE STATE: Wait for Wake Word ─────────────────────
            wake_triggered = listen_for_wakeword(threshold=0.4)
            if not wake_triggered:
                time.sleep(0.5)
                continue

            # ── ACTIVE STATE: Record & Transcribe ──────────────────
            log.info("[State: ACTIVE] Listening for voice input...")
            speak("Yes, Sir?")

            wav_file = record_audio(duration_seconds=5.0)
            user_text = transcribe_audio(wav_file)

            if not user_text.strip():
                log.info("No speech detected. Returning to IDLE.")
                continue

            log.info(f"User Spoke: '{user_text}'")

            # Check for exit command
            if any(w in user_text.lower() for w in ("goodbye", "exit daemon", "shut down daemon")):
                log.info("Shutdown command received.")
                speak("Shutting down voice daemon, Sir.")
                break

            # ── QUERY BACKEND API ─────────────────────────────────
            try:
                chat_res = httpx.post(
                    f"{BACKEND_URL}/chat",
                    json={"session_id": session_id, "text": user_text},
                    timeout=30.0,
                )
                if chat_res.status_code == 200:
                    payload = chat_res.json()
                    reply_text = payload.get("text", "")
                    log.info(f"Luna: '{reply_text}'")
                    speak(reply_text)
                else:
                    log.error(f"Backend API error ({chat_res.status_code}): {chat_res.text}")
                    speak("Sir, there was an issue processing that request.")
            except Exception as e:
                log.error(f"API request failed: {e}")
                speak("Sir, network request to backend failed.")

    except KeyboardInterrupt:
        log.info("Daemon interrupted by user.")
    finally:
        try:
            httpx.post(f"{BACKEND_URL}/session/end", json={"session_id": session_id}, timeout=3.0)
        except Exception:
            pass
        log.info("Luna Daemon Stopped.")


if __name__ == "__main__":
    run_daemon_loop()
