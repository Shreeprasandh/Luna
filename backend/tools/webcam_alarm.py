"""
Laptop Security Camera Motion Alarm Tool — Captures camera frame snapshots for security monitoring.
"""

import logging
from typing import Any
from tools.webcam import capture_webcam_snapshot

log = logging.getLogger(__name__)


def check_webcam_motion_alarm(save_path: str = "design/motion_alarm.png") -> dict[str, Any]:
    """
    Captures a webcam frame snapshot to monitor room security while away.
    """
    log.info("[Tool: check_webcam_motion_alarm] Arming webcam security alarm snapshot...")
    res = capture_webcam_snapshot(save_path)
    if res.get("status") == "success":
        res["message"] = f"Security webcam motion snapshot captured at '{res.get('image_path')}'."
    return res
