"""
Fast Local Disk File Search Tool — Rapidly searches local disk for files matching name or extension patterns.
"""

import os
import fnmatch
import logging
from typing import Any

log = logging.getLogger(__name__)


def search_local_files(query_pattern: str, search_dir: str = ".") -> dict[str, Any]:
    """
    Recursively searches local directory for files matching a wildcard pattern (e.g. '*.py', '*report*', '*.pdf').

    Args:
        query_pattern: Wildcard search pattern e.g. '*.pdf', '*invoice*'.
        search_dir: Starting root directory for search (defaults to '.').

    Returns:
        Dict with status, match count, and list of matching file paths.
    """
    abs_dir = os.path.abspath(search_dir)
    log.info(f"[Tool: search_local_files] Searching for '{query_pattern}' in '{abs_dir}'...")

    matches = []
    try:
        for root, dirs, files in os.walk(abs_dir):
            # Skip hidden folders and venv node_modules
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "venv", "__pycache__")]
            for filename in fnmatch.filter(files, query_pattern):
                matches.append(os.path.join(root, filename))
                if len(matches) >= 50:
                    break
            if len(matches) >= 50:
                break

        return {
            "status": "success",
            "search_dir": abs_dir,
            "pattern": query_pattern,
            "match_count": len(matches),
            "matches": matches,
        }
    except Exception as e:
        log.error(f"[Tool: search_local_files] Error: {e}")
        return {
            "status": "error",
            "message": f"File search failed: {str(e)}",
        }
