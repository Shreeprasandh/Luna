"""
Gmail Integration Tool — OAuth authenticated email management.
Allows Luna to list unread messages and compose/send emails on your behalf.
"""

import os
import base64
import logging
from email.mime.text import MIMEText
from typing import Any

from dotenv import load_dotenv

load_dotenv()
log = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]


def _get_gmail_service():
    """
    Loads Google OAuth credentials and builds Gmail API service instance.
    Returns None if credentials or token file are not present.
    """
    token_path = os.path.join(os.path.dirname(__file__), "..", "token.json")
    creds_path = os.path.join(os.path.dirname(__file__), "..", "google_credentials.json")

    creds = None
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        import googleapiclient.discovery

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            elif os.path.exists(creds_path):
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                creds = flow.run_local_server(port=0)
                with open(token_path, "w") as token:
                    token.write(creds.to_json())
            else:
                return None

        return googleapiclient.discovery.build("gmail", "v1", credentials=creds)

    except Exception as e:
        log.warning(f"Gmail service initialization: {e}")
        return None


def list_unread_emails(max_results: int = 5) -> dict[str, Any]:
    """
    Lists recent unread emails from your Gmail inbox.

    Args:
        max_results: Maximum number of unread emails to fetch (default 5).

    Returns:
        Dict with status, message count, and list of email dicts (id, sender, subject, snippet).
    """
    log.info(f"[Tool: list_unread_emails] Fetching top {max_results} unread emails...")
    service = _get_gmail_service()

    if not service:
        return {
            "status": "requires_auth",
            "message": "Gmail OAuth is not authorized yet. Please place google_credentials.json in backend/ folder to complete authorization.",
            "emails": [],
        }

    try:
        results = service.users().messages().list(
            userId="me", q="is:unread", maxResults=max_results
        ).execute()

        messages = results.get("messages", [])
        unread_list = []

        for msg in messages:
            msg_data = service.users().messages().get(
                userId="me", id=msg["id"], format="full"
            ).execute()

            headers = msg_data.get("payload", {}).get("headers", [])
            subject = next((h["value"] for h in headers if h["name"].lower() == "subject"), "(No Subject)")
            sender = next((h["value"] for h in headers if h["name"].lower() == "from"), "(Unknown Sender)")

            unread_list.append({
                "id": msg["id"],
                "sender": sender,
                "subject": subject,
                "snippet": msg_data.get("snippet", ""),
            })

        return {
            "status": "success",
            "count": len(unread_list),
            "emails": unread_list,
        }

    except Exception as e:
        log.error(f"[Tool: list_unread_emails] Error: {e}")
        return {
            "status": "error",
            "message": f"Failed to fetch Gmail unread messages: {str(e)}",
            "emails": [],
        }


def send_email(to: str, subject: str, body: str) -> dict[str, Any]:
    """
    Sends an email to a specified recipient using Gmail API.

    Args:
        to: Recipient email address.
        subject: Email subject line.
        body: Plain text content of the email.

    Returns:
        Dict with status, recipient, subject, and message ID.
    """
    log.info(f"[Tool: send_email] Sending email to '{to}' with subject '{subject}'")
    service = _get_gmail_service()

    if not service:
        return {
            "status": "requires_auth",
            "message": "Gmail OAuth is not authorized yet. Please place google_credentials.json in backend/ folder.",
        }

    try:
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        raw_msg = base64.urlsafe_b64encode(message.as_bytes()).decode()

        sent_msg = service.users().messages().send(
            userId="me", body={"raw": raw_msg}
        ).execute()

        return {
            "status": "success",
            "message_id": sent_msg.get("id"),
            "to": to,
            "subject": subject,
        }

    except Exception as e:
        log.error(f"[Tool: send_email] Error sending email: {e}")
        return {
            "status": "error",
            "message": f"Failed to send email: {str(e)}",
        }
