"""
Google Calendar Integration Tool — Event scheduling & agenda management.
Allows Luna to view upcoming events and schedule new appointments on your calendar.
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


def _get_calendar_service():
    """
    Loads Google OAuth credentials and builds Calendar API service instance.
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
            creds = Credentials.from_authorized_user_file(token_path, CALENDAR_SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            elif os.path.exists(creds_path):
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, CALENDAR_SCOPES)
                creds = flow.run_local_server(port=0)
                with open(token_path, "w") as token:
                    token.write(creds.to_json())
            else:
                return None

        return googleapiclient.discovery.build("calendar", "v3", credentials=creds)

    except Exception as e:
        log.warning(f"Calendar service initialization: {e}")
        return None


def list_calendar_events(max_results: int = 5) -> dict[str, Any]:
    """
    Lists upcoming events from your primary Google Calendar.

    Args:
        max_results: Maximum number of events to fetch (default 5).

    Returns:
        Dict with status, event_count, and list of event dicts (summary, start, end, location).
    """
    log.info(f"[Tool: list_calendar_events] Fetching upcoming {max_results} events...")
    service = _get_calendar_service()

    if not service:
        return {
            "status": "requires_auth",
            "message": "Google Calendar OAuth is not authorized yet. Place google_credentials.json in backend/ folder.",
            "events": [],
        }

    try:
        now = datetime.now(timezone.utc).isoformat()
        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        items = events_result.get("items", [])
        event_list = []

        for event in items:
            start = event.get("start", {}).get("dateTime") or event.get("start", {}).get("date")
            end = event.get("end", {}).get("dateTime") or event.get("end", {}).get("date")

            event_list.append({
                "id": event.get("id"),
                "summary": event.get("summary", "(No Title)"),
                "start": start,
                "end": end,
                "location": event.get("location", ""),
                "description": event.get("description", ""),
            })

        return {
            "status": "success",
            "count": len(event_list),
            "events": event_list,
        }

    except Exception as e:
        log.error(f"[Tool: list_calendar_events] Error: {e}")
        return {
            "status": "error",
            "message": f"Failed to list calendar events: {str(e)}",
            "events": [],
        }


def create_calendar_event(
    summary: str,
    start_time: str,
    end_time: str,
    description: str = "",
    location: str = "",
) -> dict[str, Any]:
    """
    Schedules a new event on your primary Google Calendar.

    Args:
        summary: Event title / summary.
        start_time: Start time in ISO format (e.g. '2026-08-08T10:00:00+05:30').
        end_time: End time in ISO format (e.g. '2026-08-08T11:00:00+05:30').
        description: Optional event description or notes.
        location: Optional location string.

    Returns:
        Dict with status, event_id, and HTML link to created event.
    """
    log.info(f"[Tool: create_calendar_event] Scheduling '{summary}' from {start_time} to {end_time}")
    service = _get_calendar_service()

    if not service:
        return {
            "status": "requires_auth",
            "message": "Google Calendar OAuth is not authorized yet. Place google_credentials.json in backend/ folder.",
        }

    try:
        event_body = {
            "summary": summary,
            "description": description,
            "location": location,
            "start": {"dateTime": start_time},
            "end": {"dateTime": end_time},
        }

        created_event = service.events().insert(
            calendarId="primary", body=event_body
        ).execute()

        return {
            "status": "success",
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
