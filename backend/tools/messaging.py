"""
Discord & Slack Webhook Notification Bridge Tool.
"""

import httpx
import logging
from typing import Any

log = logging.getLogger(__name__)


def send_webhook_message(webhook_url: str, message: str) -> dict[str, Any]:
    """
    Sends an automated notification message to a Discord or Slack webhook URL.
    """
    clean_url = webhook_url.strip()
    clean_msg = message.strip()
    log.info(f"[Tool: send_webhook_message] Dispatching webhook notification...")

    try:
        payload = {"content": clean_msg, "text": clean_msg}
        r = httpx.post(clean_url, json=payload, timeout=5.0)
        return {
            "status": "success" if r.status_code in (200, 204) else "error",
            "http_code": r.status_code,
            "message": f"Webhook message dispatched (HTTP {r.status_code}).",
        }
    except Exception as e:
        log.error(f"[Tool: send_webhook_message] Error: {e}")
        return {"status": "error", "message": f"Webhook dispatch failed: {str(e)}"}
