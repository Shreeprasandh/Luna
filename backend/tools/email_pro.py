"""
Advanced Email Draft Generator & Priority Sender Filter Tool.
"""

import logging
from typing import Any
from tools.gmail import list_unread_emails

log = logging.getLogger(__name__)

_EMAIL_DRAFTS: list[dict] = []


def create_email_draft(to: str, subject: str, body: str) -> dict[str, Any]:
    """
    Creates and stores an email draft for review before sending.
    """
    draft = {"to": to.strip(), "subject": subject.strip(), "body": body.strip()}
    _EMAIL_DRAFTS.append(draft)
    log.info(f"[Tool: create_email_draft] Created email draft for '{to}'")

    return {
        "status": "success",
        "draft": draft,
        "total_drafts": len(_EMAIL_DRAFTS),
        "message": f"Created email draft to '{to}' with subject '{subject}'.",
    }


def search_priority_emails(sender_or_keyword: str) -> dict[str, Any]:
    """
    Searches recent unread inbox emails matching sender or keyword.
    """
    clean_kw = sender_or_keyword.strip().lower()
    log.info(f"[Tool: search_priority_emails] Filtering emails for '{clean_kw}'...")
    res = list_unread_emails(max_results=10)

    if res.get("status") != "success":
        return res

    all_emails = res.get("emails", [])
    filtered = [e for e in all_emails if clean_kw in e.get("sender", "").lower() or clean_kw in e.get("subject", "").lower()]

    return {
        "status": "success",
        "query": clean_kw,
        "count": len(filtered),
        "emails": filtered,
        "message": f"Found {len(filtered)} priority emails matching '{clean_kw}'.",
    }
