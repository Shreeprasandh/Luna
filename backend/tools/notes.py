"""
Markdown Notes Vault & Knowledge Base Manager Tool.
"""

import os
import logging
from typing import Any

log = logging.getLogger(__name__)


def create_markdown_note(title: str, content: str, folder: str = "notes") -> dict[str, Any]:
    """
    Creates or appends to a local Markdown note file.

    Args:
        title: Note title (e.g. 'project_ideas').
        content: Text content.
        folder: Folder location (default 'notes').
    """
    clean_title = title.strip().replace(" ", "_").lower()
    if not clean_title.endswith(".md"):
        clean_title += ".md"

    abs_dir = os.path.abspath(folder)
    os.makedirs(abs_dir, exist_ok=True)
    file_path = os.path.join(abs_dir, clean_title)

    log.info(f"[Tool: create_markdown_note] Saving note to '{file_path}'...")
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"\n# {title.strip()}\n{content.strip()}\n")

        return {
            "status": "success",
            "file_path": file_path,
            "message": f"Saved Markdown note '{clean_title}' to folder '{folder}'.",
        }
    except Exception as e:
        log.error(f"[Tool: create_markdown_note] Error: {e}")
        return {"status": "error", "message": f"Failed to save note: {str(e)}"}


def search_markdown_notes(query: str, folder: str = "notes") -> dict[str, Any]:
    """
    Searches local Markdown notes folder for a keyword query.
    """
    abs_dir = os.path.abspath(folder)
    log.info(f"[Tool: search_markdown_notes] Searching notes in '{abs_dir}' for '{query}'...")
    matches = []

    if not os.path.exists(abs_dir):
        return {"status": "success", "count": 0, "matches": [], "message": f"Notes folder '{folder}' is empty."}

    try:
        for root, _, files in os.walk(abs_dir):
            for file in files:
                if file.endswith(".md"):
                    f_path = os.path.join(root, file)
                    with open(f_path, "r", encoding="utf-8", errors="replace") as f:
                        text = f.read()
                        if query.lower() in text.lower():
                            matches.append({"file": file, "path": f_path, "snippet": text[:300]})

        return {
            "status": "success",
            "count": len(matches),
            "matches": matches,
            "message": f"Found {len(matches)} notes matching '{query}'.",
        }
    except Exception as e:
        log.error(f"[Tool: search_markdown_notes] Error: {e}")
        return {"status": "error", "message": f"Notes search failed: {str(e)}"}
