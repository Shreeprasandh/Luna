"""
Clipboard Snippet Stash Tool — Saves named snippets from the clipboard for instant recall.
"""

import json
import logging
from typing import Any
import pyperclip

log = logging.getLogger(__name__)

_STASH: dict[str, str] = {}


def stash_clipboard_snippet(label: str) -> dict[str, Any]:
    """
    Saves current OS clipboard text under a custom label for future recall.

    Args:
        label: Name or label for the snippet (e.g. 'API Key', 'Project Goal').
    """
    clean_label = label.strip()
    log.info(f"[Tool: stash_clipboard_snippet] Stashing snippet as '{clean_label}'...")

    try:
        content = pyperclip.paste()
        if not content:
            return {"status": "error", "message": "Clipboard is currently empty."}

        _STASH[clean_label] = content
        return {
            "status": "success",
            "label": clean_label,
            "char_count": len(content),
            "message": f"Saved clipboard snippet as '{clean_label}'.",
        }
    except Exception as e:
        log.error(f"[Tool: stash_clipboard_snippet] Error: {e}")
        return {"status": "error", "message": f"Snippet stash failed: {str(e)}"}


def list_stashed_snippets() -> dict[str, Any]:
    """
    Lists all saved clipboard snippets and labels.
    """
    return {
        "status": "success",
        "count": len(_STASH),
        "snippets": [{"label": k, "preview": v[:60] + "..." if len(v) > 60 else v} for k, v in _STASH.items()],
    }
