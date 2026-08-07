"""
Speech-to-Text (STT) Engine — Local offline speech recognition using Whisper.
Model: tiny.en (fast, lightweight, CPU-friendly)
"""

import os
import wave
import tempfile
import logging
import numpy as np
import sounddevice as sd

log = logging.getLogger(__name__)

_model = None
SAMPLE_RATE = 16000


def _get_model():
    global _model
    if _model is None:
        log.info("Loading local Whisper STT model (tiny.en)...")
        import whisper
        _model = whisper.load_model("tiny.en")
        log.info("Whisper STT model loaded.")
    return _model


def record_audio(duration_seconds: float = 4.0, sample_rate: int = SAMPLE_RATE) -> str:
    """
    Records audio from the default microphone for a given duration.

    Args:
        duration_seconds: Duration to record in seconds.
        sample_rate: Sampling frequency (default 16000 Hz).

    Returns:
        Path to temporary WAV audio file.
    """
    log.info(f"Listening for {duration_seconds}s...")
    audio_data = sd.rec(
        int(duration_seconds * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )
    sd.wait()

    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_path = temp_wav.name
    temp_wav.close()

    with wave.open(temp_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    return temp_path


def transcribe_audio(wav_path: str) -> str:
    """
    Transcribes a WAV audio file into text using local Whisper.

    Args:
        wav_path: Path to input WAV file.

    Returns:
        Transcribed text.
    """
    try:
        model = _get_model()
        result = model.transcribe(wav_path, fp16=False)
        text = (result.get("text") or "").strip()
        log.info(f"Transcribed: '{text}'")
        return text
    except Exception as e:
        log.error(f"STT Transcription error: {e}")
        return ""
    finally:
        if os.path.exists(wav_path):
            try:
                os.remove(wav_path)
            except Exception:
                pass
