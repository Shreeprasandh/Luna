"""
Webcam Physical Vision Tool — Captures a webcam image for Gemini Multimodal Vision analysis.
Allows Luna to see physical objects or inspect Sir's environment upon request.
"""

import os
import cv2
import logging
from typing import Any

log = logging.getLogger(__name__)


def capture_webcam_snapshot(save_path: str = "design/webcam_snapshot.png") -> dict[str, Any]:
    """
    Captures a frame from the primary webcam camera and saves it to disk.

    Args:
        save_path: Destination image path (default 'design/webcam_snapshot.png').

    Returns:
        Dict with status, image_path, and dimensions.
    """
    abs_path = os.path.abspath(save_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    log.info(f"[Tool: capture_webcam_snapshot] Accessing webcam camera...")

    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            return {"status": "error", "message": "Could not access webcam device."}

        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            return {"status": "error", "message": "Failed to read frame from webcam."}

        cv2.imwrite(abs_path, frame)
        height, width, _ = frame.shape

        log.info(f"Webcam snapshot saved to '{abs_path}' ({width}x{height})")
        return {
            "status": "success",
            "image_path": abs_path,
            "width": width,
            "height": height,
            "message": f"Webcam snapshot saved successfully to {save_path}.",
        }
    except Exception as e:
        log.error(f"[Tool: capture_webcam_snapshot] Error: {e}")
        return {
            "status": "error",
            "message": f"Webcam capture failed: {str(e)}",
        }
