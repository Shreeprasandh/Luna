"""
Clipboard Vault Tool — Stores multi-item clipboard history.
"""

import logging
from typing import Any

log = logging.getLogger(__name__)

_VAULT_HISTORY: list[str] = []


def push_to_clipboard_vault(text: str) -> dict[str, Any]:
    """
    Pushes text into the multi-item clipboard vault history.
    """
    clean_text = text.strip()
    if clean_text and clean_text not in _VAULT_HISTORY:
        _VAULT_HISTORY.insert(0, clean_text)
        if len(_VAULT_HISTORY) > 50:
            _VAULT_HISTORY.pop()

    return {
        "status": "success",
        "vault_size": len(_VAULT_HISTORY),
        "message": f"Pushed snippet to clipboard vault ({len(_VAULT_HISTORY)} items stored).",
    }


def get_clipboard_vault_history() -> dict[str, Any]:
    """
    Retrieves stored clipboard vault items.
    """
    return {
        "status": "success",
        "count": len(_VAULT_HISTORY),
        "history": _VAULT_HISTORY[:15],
    }
