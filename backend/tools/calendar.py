"""
Google Calendar Integration Tool — Multi-account event scheduling & agenda management.
Allows Luna to view upcoming events and schedule appointments across multiple accounts.
"""

import os
import logging
from datetime import datetime, timezone
from typing import Any

from dotenv import load_dotenv

load_dotenv()
log = logging.getLogger(__name__)

CALENDAR_SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.readonly",
]


def _get_calendar_services() -> list[tuple[str, Any]]:
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
                    creds = Credentials.from_authorized_user_file(token_path, CALENDAR_SCOPES)
                except Exception:
                    creds = None

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                    except Exception:
                        creds = None
                elif os.path.exists(creds_path):
                    flow = InstalledAppFlow.from_client_secrets_file(creds_path, CALENDAR_SCOPES)
                    creds = flow.run_local_server(port=0)
                    with open(token_path, "w") as token:
                        token.write(creds.to_json())

            if creds and creds.valid:
                srv = googleapiclient.discovery.build("calendar", "v3", credentials=creds)
                services.append((tag, srv))

        return services

    except Exception as e:
        log.warning(f"Calendar multi-account service initialization error: {e}")
        return []


def list_calendar_events(max_results: int = 5, account: str | None = None) -> dict[str, Any]:
    """
    Lists upcoming events across all connected Google Calendars (or a specific account).

    Args:
        max_results: Maximum events per calendar (default 5).
        account: Optional account tag e.g. 'work' | 'personal' | None (for all).

    Returns:
        Dict with status, count, and list of event dicts.
    """
    log.info(f"[Tool: list_calendar_events] Fetching upcoming events (account filter: {account})...")
    services = _get_calendar_services()

    if not services:
        return {
            "status": "requires_auth",
            "message": "No Google Calendar OAuth credentials found. Place google_credentials_work.json or google_credentials_personal.json in backend/ folder.",
            "events": [],
        }

    all_events = []
    now = datetime.now(timezone.utc).isoformat()

    for tag, service in services:
        if account and account.lower() not in (tag.lower(), "all"):
            continue

        try:
            events_result = service.events().list(
                calendarId="primary",
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            ).execute()

            items = events_result.get("items", [])

            for event in items:
                start = event.get("start", {}).get("dateTime") or event.get("start", {}).get("date")
                end = event.get("end", {}).get("dateTime") or event.get("end", {}).get("date")

                all_events.append({
                    "account": tag,
                    "id": event.get("id"),
                    "summary": event.get("summary", "(No Title)"),
                    "start": start,
                    "end": end,
                    "location": event.get("location", ""),
                    "description": event.get("description", ""),
                })

        except Exception as e:
            log.error(f"[Tool: list_calendar_events] Error reading calendar '{tag}': {e}")

    # Sort combined events chronologically by start time
    all_events.sort(key=lambda x: x.get("start") or "")

    return {
        "status": "success",
        "count": len(all_events),
        "events": all_events,
    }


def create_calendar_event(
    summary: str,
    start_time: str,
    end_time: str,
    description: str = "",
    location: str = "",
    account: str = "primary",
) -> dict[str, Any]:
    """
    Schedules a new event on a specified Google Calendar account ('work', 'personal', or 'primary').
    """
    log.info(f"[Tool: create_calendar_event] Scheduling '{summary}' on account '{account}'")
    services = _get_calendar_services()

    if not services:
        return {
            "status": "requires_auth",
            "message": "No Google Calendar OAuth credentials found in backend/ folder.",
        }

    target_service = None
    for tag, srv in services:
        if tag.lower() == account.lower():
            target_service = srv
            break

    if not target_service:
        tag, target_service = services[0]

    try:
        event_body = {
            "summary": summary,
            "description": description,
            "location": location,
            "start": {"dateTime": start_time},
            "end": {"dateTime": end_time},
        }

        created_event = target_service.events().insert(
            calendarId="primary", body=event_body
        ).execute()

        return {
            "status": "success",
            "scheduled_on_account": tag,
            "event_id": created_event.get("id"),
            "summary": summary,
            "html_link": created_event.get("htmlLink"),
        }

    except Exception as e:
        log.error(f"[Tool: create_calendar_event] Error: {e}")
        return {
            "status": "error",
            "message": f"Failed to create calendar event: {str(e)}",
        }
