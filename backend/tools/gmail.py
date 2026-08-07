"""
Gmail Integration Tool — Multi-account OAuth authenticated email management.
Supports primary, work, and personal Google accounts seamlessly.
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


def _get_gmail_services() -> list[tuple[str, Any]]:
    """
    Loads all available Google OAuth credentials files in backend/ folder.
    Supports: google_credentials.json, google_credentials_work.json, google_credentials_personal.json
    Returns a list of (account_tag, service_instance) tuples.
    """
    backend_dir = os.path.join(os.path.dirname(__file__), "..")
    
    cred_files = [
        ("primary", "google_credentials.json", "token.json"),
        ("work", "google_credentials_work.json", "token_work.json"),
        ("personal", "google_credentials_personal.json", "token_personal.json"),
        ("luna", "google_credentials_luna.json", "token_luna.json"),
    ]

    services = []

    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        import googleapiclient.discovery

        for tag, cred_filename, token_filename in cred_files:
            creds_path = os.path.join(backend_dir, cred_filename)
            token_path = os.path.join(backend_dir, token_filename)

            creds = None
            if os.path.exists(token_path):
                try:
                    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
                except Exception:
                    creds = None

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                    except Exception:
                        creds = None
                elif os.path.exists(creds_path):
                    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                    with open(token_path, "w") as token:
                        token.write(creds.to_json())

            if creds and creds.valid:
                srv = googleapiclient.discovery.build("gmail", "v1", credentials=creds)
                services.append((tag, srv))

        return services

    except Exception as e:
        log.warning(f"Gmail multi-account service initialization error: {e}")
        return []


def list_unread_emails(max_results: int = 5, account: str | None = None) -> dict[str, Any]:
    """
    Lists recent unread emails across all connected Gmail accounts (or a specific account).

    Args:
        max_results: Maximum unread emails per account (default 5).
        account: Optional filter e.g. 'work' | 'personal' | None (for all).

    Returns:
        Dict with status, count, and list of email dicts.
    """
    log.info(f"[Tool: list_unread_emails] Fetching unread emails (account filter: {account})...")
    services = _get_gmail_services()

    if not services:
        return {
            "status": "requires_auth",
            "message": "No Google OAuth credentials found. Place google_credentials_work.json or google_credentials_personal.json in backend/ folder.",
            "emails": [],
        }

    all_emails = []

    for tag, service in services:
        if account and account.lower() not in (tag.lower(), "all"):
            continue

        try:
            results = service.users().messages().list(
                userId="me", q="is:unread", maxResults=max_results
            ).execute()

            messages = results.get("messages", [])

            for msg in messages:
                msg_data = service.users().messages().get(
                    userId="me", id=msg["id"], format="full"
                ).execute()

                headers = msg_data.get("payload", {}).get("headers", [])
                subject = next((h["value"] for h in headers if h["name"].lower() == "subject"), "(No Subject)")
                sender = next((h["value"] for h in headers if h["name"].lower() == "from"), "(Unknown Sender)")

                all_emails.append({
                    "account": tag,
                    "id": msg["id"],
                    "sender": sender,
                    "subject": subject,
                    "snippet": msg_data.get("snippet", ""),
                })

        except Exception as e:
            log.error(f"[Tool: list_unread_emails] Error reading account '{tag}': {e}")

    return {
        "status": "success",
        "count": len(all_emails),
        "emails": all_emails,
    }


def send_email(to: str, subject: str, body: str, account: str = "primary") -> dict[str, Any]:
    """
    Sends an email from a specified account ('work', 'personal', or 'primary').
    """
    log.info(f"[Tool: send_email] Sending email to '{to}' via account '{account}'")
    services = _get_gmail_services()

    if not services:
        return {
            "status": "requires_auth",
            "message": "No Google OAuth credentials found in backend/ folder.",
        }

    # Find matching account service
    target_service = None
    for tag, srv in services:
        if tag.lower() == account.lower():
            target_service = srv
            break

    if not target_service:
        # Default to first available service if specified tag not matched
        tag, target_service = services[0]

    try:
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        raw_msg = base64.urlsafe_b64encode(message.as_bytes()).decode()

        sent_msg = target_service.users().messages().send(
            userId="me", body={"raw": raw_msg}
        ).execute()

        return {
            "status": "success",
            "sent_from_account": tag,
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
