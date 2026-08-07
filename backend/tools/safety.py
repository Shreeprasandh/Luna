"""
Safety & Action Governance Guard — Production-Grade Security & Permission Enforcement.

Categorizes tools into Low-Risk, High-Risk, and Extreme-Risk:
- Low-Risk (Autonomous Execution): web_search, image_search, read_file, list_directory,
  list_unread_emails, list_calendar_events, get_system_health, git_status.
- High-Risk (Requires Explicit User Permission): write_file, execute_python_code,
  send_email, create_calendar_event, git_commit_and_push.
- Extreme-Risk (Requires Master Password "ONE PIECE"): Full drive deletion, disk wiping, drop all schemas.

Includes Path Traversal Protection & Security Validation.
"""

import os
import logging
from typing import Any

log = logging.getLogger(__name__)

# Allowed workspace root directory
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

MASTER_EMERGENCY_PASSWORD = "ONE PIECE"

HIGH_RISK_TOOLS = {
    "write_file": "Modifying or writing files on local disk",
    "execute_python_code": "Executing code in local Python sandbox",
    "send_email": "Sending emails via Gmail",
    "create_calendar_event": "Scheduling new calendar appointments",
    "git_commit_and_push": "Committing and pushing changes to GitHub repository",
}

EXTREME_RISK_PATTERNS = [
    "delete_drive", "format_", "rmdir /s", "rm -rf /", "wipe_disk", "drop_database", "delete_all"
]


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
    Validates tool execution parameters for safety, path bounds, and emergency password requirement.

    Returns:
        Dict with 'allowed': bool, 'is_high_risk': bool, 'reason': str
    """
    is_high_risk = tool_name in HIGH_RISK_TOOLS
    risk_description = HIGH_RISK_TOOLS.get(tool_name, "")

    # Extreme Risk Check — Requires password "ONE PIECE"
    arg_str = str(arguments).lower()
    for pattern in EXTREME_RISK_PATTERNS:
        if pattern in arg_str:
            pwd = arguments.get("password") or ""
            if pwd != MASTER_EMERGENCY_PASSWORD:
                log.warning(f"EXTREME SECURITY ALERT: Destructive action blocked (pattern: '{pattern}')")
                return {
                    "allowed": False,
                    "is_high_risk": True,
                    "reason": f"EXTREME RISK BLOCKED: Full drive deletion or administrative wiping requires Sir to explicitly enter the Master Emergency Password '{MASTER_EMERGENCY_PASSWORD}'.",
                }

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
