"""
Tool Registry — central manager for tool schema definitions and execution dispatch.
Includes: Web search, Image search, File system, Gmail, and Google Calendar tools.
"""

import json
import logging
from typing import Any, Callable

from tools.search import web_search, image_search
from tools.files import read_file, write_file, list_directory
from tools.gmail import list_unread_emails, send_email
from tools.calendar import list_calendar_events, create_calendar_event

log = logging.getLogger(__name__)

# Map of tool_name -> execution function
_TOOL_MAP: dict[str, Callable[..., dict[str, Any]]] = {
    "web_search": web_search,
    "image_search": image_search,
    "read_file": read_file,
    "write_file": write_file,
    "list_directory": list_directory,
    "list_unread_emails": list_unread_emails,
    "send_email": send_email,
    "list_calendar_events": list_calendar_events,
    "create_calendar_event": create_calendar_event,
}

# OpenAI-compatible function tool definitions
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Searches the web for up-to-date information, news, current facts, or articles.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search term or query to look up on the web."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "image_search",
            "description": "Searches for images on the web when the user asks to see an image or visual of a concept, object, or person.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The visual search term or image query."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a local file on the user's computer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The file path to read."
                    }
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Creates or overwrites a file on the user's computer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The target file path to create/overwrite."
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file."
                    }
                },
                "required": ["filepath", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "Lists files and folders inside a local directory on the user's computer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dirpath": {
                        "type": "string",
                        "description": "The directory path to list (defaults to '.')."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_unread_emails",
            "description": "Lists recent unread emails from the user's Gmail inbox.",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of unread emails to fetch (default 5)."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Sends an email to a recipient address via Gmail.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "Recipient email address."
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line."
                    },
                    "body": {
                        "type": "string",
                        "description": "Email body content."
                    }
                },
                "required": ["to", "subject", "body"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_calendar_events",
            "description": "Lists upcoming events from the user's primary Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of upcoming events to list (default 5)."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_calendar_event",
            "description": "Schedules a new appointment or event on the user's Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "Title or summary of the event."
                    },
                    "start_time": {
                        "type": "string",
                        "description": "Start time in ISO 8601 format e.g. 2026-08-08T10:00:00+05:30"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "End time in ISO 8601 format e.g. 2026-08-08T11:00:00+05:30"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional notes or event description."
                    }
                },
                "required": ["summary", "start_time", "end_time"]
            }
        }
    }
]


def execute_tool(name: str, arguments: dict[str, Any] | str) -> dict[str, Any]:
    """
    Dispatches execution of a registered tool by name with arguments.
    """
    if name not in _TOOL_MAP:
        log.error(f"Unknown tool requested: '{name}'")
        return {"status": "error", "message": f"Unknown tool: '{name}'"}

    if isinstance(arguments, str):
        try:
            arguments = json.loads(arguments)
        except Exception as e:
            log.error(f"Failed to parse tool arguments for '{name}': {e}")
            return {"status": "error", "message": f"Invalid arguments format: {e}"}

    log.info(f"Executing tool '{name}' with args: {arguments}")
    try:
        handler = _TOOL_MAP[name]
        return handler(**arguments)
    except Exception as e:
        log.error(f"Execution error in tool '{name}': {e}")
        return {"status": "error", "message": f"Tool execution failed: {str(e)}"}
