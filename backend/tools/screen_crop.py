"""
Region Screen Crop & Visual Analyzer Tool.
"""

import logging
from typing import Any
from PIL import ImageGrab

log = logging.getLogger(__name__)


def crop_screen_region(x: int = 0, y: int = 0, width: int = 800, height: int = 600, save_path: str = "design/cropped_region.png") -> dict[str, Any]:
    """
    Crops a specific monitor region (x, y, width, height) and saves it for visual analysis.
    """
    log.info(f"[Tool: crop_screen_region] Cropping screen region ({x}, {y}, {width}, {height})...")
    try:
        box = (x, y, x + width, y + height)
        img = ImageGrab.grab(bbox=box)
        img.save(save_path)
        return {
            "status": "success",
            "image_path": save_path,
            "bbox": box,
            "message": f"Cropped screen region saved to '{save_path}'.",
        }
    except Exception as e:
        log.error(f"[Tool: crop_screen_region] Error: {e}")
        return {"status": "error", "message": f"Screen crop failed: {str(e)}"}
