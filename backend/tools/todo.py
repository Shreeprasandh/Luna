"""
Google Tasks & Todoist Task Manager Tool.
"""

import logging
from typing import Any

log = logging.getLogger(__name__)

_TODO_ITEMS: list[dict] = []


def add_todo_task(title: str, due_date: str = "today") -> dict[str, Any]:
    """
    Adds a checkable task item to your daily to-do list.
    """
    item = {"title": title.strip(), "due_date": due_date.strip(), "completed": False}
    _TODO_ITEMS.append(item)
    log.info(f"[Tool: add_todo_task] Added task: '{title}' (due {due_date})")

    return {
        "status": "success",
        "task": item,
        "total_tasks": len(_TODO_ITEMS),
        "message": f"Added task '{title}' to your to-do list.",
    }


def list_todo_tasks() -> dict[str, Any]:
    """
    Retrieves active to-do list tasks.
    """
    return {
        "status": "success",
        "count": len(_TODO_ITEMS),
        "tasks": _TODO_ITEMS,
        "message": f"Retrieved {len(_TODO_ITEMS)} active to-do tasks.",
    }
