"""
Tool Registry — central manager for tool schema definitions and execution dispatch.
Includes: Web search, Image search, File system, Gmail, Calendar, Browser automation,
Code execution, Screen Vision inspection, System Hardware monitor, Autonomous Git agent,
Proactive Task Scheduler, App Launcher, Clipboard Manager, and Network Diagnostics.
"""

import json
import logging
from typing import Any, Callable

from tools.search import web_search, image_search
from tools.files import read_file, write_file, list_directory
from tools.gmail import list_unread_emails, send_email
from tools.calendar import list_calendar_events, create_calendar_event
from tools.browser import browse_url, take_screenshot
from tools.code import execute_python_code
from tools.screen import capture_desktop_screen, analyze_screen_image
from tools.system import get_system_health
from tools.git_agent import git_status, git_commit_and_push
from tools.scheduler import schedule_reminder, list_scheduled_tasks
from tools.app_launcher import launch_app, open_url_in_browser
from tools.clipboard import get_clipboard_text, set_clipboard_text
from tools.network import get_network_diagnostics

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
    "browse_url": browse_url,
    "take_screenshot": take_screenshot,
    "execute_python_code": execute_python_code,
    "capture_desktop_screen": capture_desktop_screen,
    "analyze_screen_image": analyze_screen_image,
    "get_system_health": get_system_health,
    "git_status": git_status,
    "git_commit_and_push": git_commit_and_push,
    "schedule_reminder": schedule_reminder,
    "list_scheduled_tasks": list_scheduled_tasks,
    "launch_app": launch_app,
    "open_url_in_browser": open_url_in_browser,
    "get_clipboard_text": get_clipboard_text,
    "set_clipboard_text": set_clipboard_text,
    "get_network_diagnostics": get_network_diagnostics,
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
    },
    {
        "type": "function",
        "function": {
            "name": "browse_url",
            "description": "Navigates to a webpage using Playwright headless browser and extracts its text content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The webpage URL to visit and scrape."
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "take_screenshot",
            "description": "Captures a visual screenshot of a webpage and saves it locally.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The webpage URL to capture."
                    },
                    "save_path": {
                        "type": "string",
                        "description": "Destination file path (default 'design/page_preview.png')."
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_python_code",
            "description": "Executes a Python code snippet in an isolated sandbox and returns stdout/stderr.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The Python code snippet to execute."
                    }
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "capture_desktop_screen",
            "description": "Captures a full screenshot of the user's primary monitor screen.",
            "parameters": {
                "type": "object",
                "properties": {
                    "save_path": {
                        "type": "string",
                        "description": "Destination file path for screenshot (default 'design/screen_capture.png')."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_screen_image",
            "description": "Uses Gemini Multimodal Vision to inspect and analyze an image file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "File path to the image to analyze."
                    },
                    "prompt": {
                        "type": "string",
                        "description": "What to look for or question about the visual screen content."
                    }
                },
                "required": ["image_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_system_health",
            "description": "Inspects real-time PC hardware metrics including CPU, RAM, Disk usage %, and top processes.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "git_status",
            "description": "Inspects current Git repository branch and modified/untracked files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Path to local Git repo (default '.')."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "git_commit_and_push",
            "description": "Stages all changes, creates a commit with the provided message, and pushes to remote.",
            "parameters": {
                "type": "object",
                "properties": {
                    "commit_message": {
                        "type": "string",
                        "description": "Git commit message."
                    },
                    "repo_path": {
                        "type": "string",
                        "description": "Path to local Git repo (default '.')."
                    }
                },
                "required": ["commit_message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_reminder",
            "description": "Schedules a timed proactive reminder or notification to trigger after a delay in seconds.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_description": {
                        "type": "string",
                        "description": "The reminder text or task description."
                    },
                    "delay_seconds": {
                        "type": "integer",
                        "description": "Time delay in seconds from now before triggering reminder."
                    }
                },
                "required": ["task_description", "delay_seconds"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_scheduled_tasks",
            "description": "Lists all active background reminders and scheduled tasks.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "launch_app",
            "description": "Launches a desktop application by name (e.g. 'code', 'chrome', 'notepad', 'calculator', 'spotify').",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "The application name to launch."
                    }
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_url_in_browser",
            "description": "Opens a website URL in the user's default desktop browser.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The website URL to open."
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_clipboard_text",
            "description": "Reads text content currently stored on the user's OS clipboard.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_clipboard_text",
            "description": "Copies text content to the user's OS clipboard.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text content to copy to clipboard."
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_network_diagnostics",
            "description": "Inspects local IP address, hostname, and tests internet ping latency.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


def execute_tool(name: str, arguments: dict[str, Any] | str) -> dict[str, Any]:
    """
    Dispatches execution of a registered tool by name with arguments.
    Enforces Security & Path Traversal Validation before execution.
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

    # Security & Path Traversal Validation Guard
    from tools.safety import validate_tool_execution
    safety_check = validate_tool_execution(name, arguments)
    if not safety_check["allowed"]:
        log.warning(f"Tool execution blocked by Safety Guard: {safety_check['reason']}")
        return {"status": "error", "message": safety_check["reason"]}

    log.info(f"Executing tool '{name}' with args: {arguments}")
    try:
        handler = _TOOL_MAP[name]
        return handler(**arguments)
    except Exception as e:
        log.error(f"Execution error in tool '{name}': {e}")
        return {"status": "error", "message": f"Tool execution failed: {str(e)}"}
