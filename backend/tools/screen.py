"""
Screen Inspection & Vision Tool — Captures desktop screen and inspects visual contents.
Uses mss screen capture + Gemini Vision multimodal model to analyze desktop state.
"""

import os
import logging
from typing import Any
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
log = logging.getLogger(__name__)


def capture_desktop_screen(save_path: str = "design/screen_capture.png") -> dict[str, Any]:
    """
    Captures a full screenshot of the user's primary monitor and saves it locally.

    Args:
        save_path: Local destination path for the screenshot image file.

    Returns:
        Dict with status, image_path, and dimensions.
    """
    abs_save_path = os.path.abspath(save_path)
    os.makedirs(os.path.dirname(abs_save_path), exist_ok=True)
    log.info(f"[Tool: capture_desktop_screen] Capturing desktop to: '{abs_save_path}'")

    try:
        import mss
        with mss.mss() as sct:
            monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img.save(abs_save_path, "PNG")
            width, height = img.size

            return {
                "status": "success",
                "image_path": abs_save_path,
                "dimensions": f"{width}x{height}",
            }
    except Exception as e:
        log.error(f"[Tool: capture_desktop_screen] Error capturing screen: {e}")
        return {
            "status": "error",
            "message": f"Desktop screen capture requires active user session: {str(e)}",
        }


def analyze_screen_image(
    image_path: str = "design/screen_capture.png",
    prompt: str = "Describe what is visible on the user's screen in 2-3 clear sentences.",
) -> dict[str, Any]:
    """
    Analyzes an image file (e.g. desktop screenshot) using Gemini Vision multimodal model.

    Args:
        image_path: Path to the image file to inspect.
        prompt: Question or prompt describing what to look for in the image.

    Returns:
        Dict with status, image_path, and visual_analysis text.
    """
    abs_image_path = os.path.abspath(image_path)
    if not os.path.exists(abs_image_path):
        return {
            "status": "error",
            "message": f"Image file not found: {image_path}",
        }

    log.info(f"[Tool: analyze_screen_image] Analyzing image '{abs_image_path}' with prompt: '{prompt}'")

    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return {
                "status": "error",
                "message": "GEMINI_API_KEY is not configured in backend/.env for Vision analysis.",
            }

        genai.configure(api_key=api_key)
        vision_models = ["gemini-2.0-flash", "gemini-2.0-flash-lite"]
        image_data = Image.open(abs_image_path)

        analysis_text = None
        last_err = None

        for model_name in vision_models:
            for attempt in range(2):
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content([prompt, image_data])
                    if response and response.text:
                        analysis_text = response.text.strip()
                        log.info(f"Vision analysis successful using model '{model_name}'.")
                        break
                except Exception as err:
                    last_err = err
                    if "429" in str(err) and attempt == 0:
                        import time
                        time.sleep(2)
                        continue
                    log.warning(f"Vision model '{model_name}' failed: {err}. Trying fallback...")
            if analysis_text:
                break

        if not analysis_text:
            return {
                "status": "error",
                "message": f"Vision analysis failed across models: {last_err}",
            }

        return {
            "status": "success",
            "image_path": abs_image_path,
            "analysis": analysis_text,
        }

    except Exception as e:
        log.error(f"[Tool: analyze_screen_image] Vision analysis error: {e}")
        return {
            "status": "error",
            "message": f"Vision analysis failed: {str(e)}",
        }


def get_screen_pixel_color(x: int = 100, y: int = 100) -> dict[str, Any]:
    """
    Captures screen and returns the exact Hex color code and RGB values of the pixel at coordinates (x, y).

    Args:
        x: Horizontal X coordinate on screen.
        y: Vertical Y coordinate on screen.

    Returns:
        Dict with status, hex_color, and rgb values.
    """
    log.info(f"[Tool: get_screen_pixel_color] Inspecting pixel at ({x}, {y})...")
    cap = capture_desktop_screen("design/pixel_inspect.png")
    if cap.get("status") != "success":
        return cap

    try:
        img = Image.open(cap["image_path"])
        width, height = img.size
        target_x = max(0, min(width - 1, x))
        target_y = max(0, min(height - 1, y))

        r, g, b = img.getpixel((target_x, target_y))[:3]
        hex_code = f"#{r:02x}{g:02x}{b:02x}".upper()

        return {
            "status": "success",
            "coordinates": {"x": target_x, "y": target_y},
            "hex_color": hex_code,
            "rgb": {"r": r, "g": g, "b": b},
            "message": f"Pixel color at ({target_x}, {target_y}) is {hex_code} (RGB: {r}, {g}, {b}).",
        }
    except Exception as e:
        log.error(f"[Tool: get_screen_pixel_color] Error: {e}")
        return {
            "status": "error",
            "message": f"Pixel inspection failed: {str(e)}",
        }
