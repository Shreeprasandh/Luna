"""
Proactive Autonomous Task Scheduler Tool — Timed reminders & background task triggers.
Allows Luna to schedule proactive reminders and timed actions for Sir.
"""

import time
import logging
import threading
from datetime import datetime, timedelta
from typing import Any

log = logging.getLogger(__name__)

_scheduled_tasks: list[dict[str, Any]] = []
_lock = threading.Lock()


def schedule_reminder(task_description: str, delay_seconds: int) -> dict[str, Any]:
    """
    Schedules a proactive reminder or notification to trigger after a specified delay in seconds.

    Args:
        task_description: Plain text description of the reminder or task.
        delay_seconds: Time delay in seconds from now.

    Returns:
        Dict with status, task_id, trigger_time, and description.
    """
    trigger_time = datetime.now() + timedelta(seconds=delay_seconds)
    trigger_str = trigger_time.strftime("%I:%M:%S %p")
    task_id = f"task_{int(time.time())}"

    task = {
        "id": task_id,
        "description": task_description,
        "trigger_time": trigger_str,
        "delay_seconds": delay_seconds,
        "status": "scheduled",
    }

    with _lock:
        _scheduled_tasks.append(task)

    log.info(f"[Tool: schedule_reminder] Scheduled '{task_description}' for {trigger_str}")

    def _trigger():
        time.sleep(delay_seconds)
        log.info(f"[PROACTIVE REMINDER TRIGGERED] Sir, reminder: {task_description}")
        with _lock:
            task["status"] = "completed"

    thread = threading.Thread(target=_trigger, daemon=True)
    thread.start()

    return {
        "status": "success",
        "task_id": task_id,
        "description": task_description,
        "scheduled_for": trigger_str,
    }


def list_scheduled_tasks() -> dict[str, Any]:
    """
    Lists all active background reminders and scheduled tasks.
    """
    with _lock:
        active = [t for t in _scheduled_tasks if t["status"] == "scheduled"]

    return {
        "status": "success",
        "count": len(active),
        "tasks": active,
    }
