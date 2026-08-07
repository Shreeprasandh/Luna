"""
Clipboard Manager Tool — Reads and writes content to the operating system clipboard.
Allows Luna to inspect text copied by Sir or push generated content directly to clipboard.
"""

import logging
from typing import Any
import pyperclip

log = logging.getLogger(__name__)


def get_clipboard_text() -> dict[str, Any]:
    """
    Reads and returns text content currently stored in the OS clipboard.
    """
    log.info("[Tool: get_clipboard_text] Reading OS clipboard...")
    try:
        content = pyperclip.paste()
        return {
            "status": "success",
            "content": content,
            "char_count": len(content) if content else 0,
        }
    except Exception as e:
        log.error(f"[Tool: get_clipboard_text] Error: {e}")
        return {
            "status": "error",
            "message": f"Failed to read clipboard: {str(e)}",
        }


def set_clipboard_text(text: str) -> dict[str, Any]:
    """
    Copies text content to the OS clipboard.

    Args:
        text: Plain text content to copy.
    """
    log.info("[Tool: set_clipboard_text] Copying text to OS clipboard...")
    try:
        pyperclip.copy(text)
        return {
            "status": "success",
            "message": "Copied text to clipboard successfully.",
            "char_count": len(text),
        }
    except Exception as e:
        log.error(f"[Tool: set_clipboard_text] Error: {e}")
        return {
            "status": "error",
            "message": f"Failed to set clipboard: {str(e)}",
        }
