"""
Wake Word Engine — Local OpenWakeWord listener.
Monitors microphone stream with zero API cost, minimal CPU footprint.
"""

import logging
import numpy as np
import sounddevice as sd

log = logging.getLogger(__name__)

_oww_model = None
SAMPLE_RATE = 16000
CHUNK_SIZE = 1280  # 80ms chunk for OpenWakeWord


def _get_oww_model():
    global _oww_model
    if _oww_model is None:
        log.info("Loading OpenWakeWord model...")
        from openwakeword.model import Model
        # Load default pre-trained wake word models (e.g. 'hey_jarvis' or 'alexa')
        _oww_model = Model(inference_framework="onnx")
        log.info("OpenWakeWord model loaded.")
    return _oww_model


def listen_for_wakeword(threshold: float = 0.5, timeout_seconds: float | None = None) -> bool:
    """
    Listens continuously for the wake word signal.

    Args:
        threshold: Detection confidence threshold (0.0 to 1.0).
        timeout_seconds: Max seconds to listen before returning False (None for infinite).

    Returns:
        True if wake word detected, False on timeout or interrupt.
    """
    log.info("Entering IDLE state — listening for wake word...")
    oww = _get_oww_model()
    
    detected = False

    def audio_callback(indata, frames, time_info, status):
        nonlocal detected
        if detected:
            return

        audio_chunk = (indata[:, 0] * 32767).astype(np.int16)
        prediction = oww.predict(audio_chunk)

        # Check score across all loaded wake word models
        for model_name, scores in prediction.items():
            score = scores if isinstance(scores, (float, int)) else max(scores)
            if score >= threshold:
                log.info(f"Wake word detected! Model: {model_name} (Score: {score:.2f})")
                detected = True
                break

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            blocksize=CHUNK_SIZE,
            callback=audio_callback,
        ):
            while not detected:
                sd.sleep(100)
        return True
    except Exception as e:
        log.error(f"Wake word listener error: {e}")
        return False
