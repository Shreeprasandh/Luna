"""
Safety & Action Governance Guard — Production-Grade Security & Permission Enforcement.

Categorizes tools into Low-Risk vs High-Risk:
- Low-Risk (Autonomous Execution): web_search, image_search, read_file, list_directory,
  list_unread_emails, list_calendar_events, get_system_health, git_status.
- High-Risk (Requires Explicit User Permission): write_file, execute_python_code,
  send_email, create_calendar_event, git_commit_and_push.

Includes Path Traversal Protection & Security Validation.
"""

import os
import logging
from typing import Any

log = logging.getLogger(__name__)

# Allowed workspace root directory
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

HIGH_RISK_TOOLS = {
    "write_file": "Modifying or writing files on local disk",
    "execute_python_code": "Executing code in local Python sandbox",
    "send_email": "Sending emails via Gmail",
    "create_calendar_event": "Scheduling new calendar appointments",
    "git_commit_and_push": "Committing and pushing changes to GitHub repository",
}


def is_safe_path(filepath: str) -> bool:
    """
    Path Traversal Protection — Ensures file access remains within safe project boundaries.
    Prevents path traversal attacks trying to access C:\\Windows or sensitive system files.
    """
    try:
        abs_target = os.path.abspath(filepath)
        # Check if target is inside WORKSPACE_ROOT or user's project directory
        common_prefix = os.path.commonpath([abs_target, WORKSPACE_ROOT])
        return common_prefix == WORKSPACE_ROOT
    except Exception:
        return False


def validate_tool_execution(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """
    Validates tool execution parameters for safety, path bounds, and permission requirement.

    Returns:
        Dict with 'allowed': bool, 'is_high_risk': bool, 'reason': str
    """
    is_high_risk = tool_name in HIGH_RISK_TOOLS
    risk_description = HIGH_RISK_TOOLS.get(tool_name, "")

    # Path traversal validation for file tools
    if tool_name in ("read_file", "write_file", "list_directory"):
        target = arguments.get("filepath") or arguments.get("dirpath") or ""
        if target and not is_safe_path(target):
            log.warning(f"Security Alert: Path traversal attempt blocked for path '{target}'")
            return {
                "allowed": False,
                "is_high_risk": True,
                "reason": f"Access denied: Target path '{target}' is outside safe workspace boundaries.",
            }

    return {
        "allowed": True,
        "is_high_risk": is_high_risk,
        "description": risk_description,
    }
