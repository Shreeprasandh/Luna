"""
GitHub Repository Issue & PR Tracker Tool — Tracks GitHub repository status and active branches.
"""

import logging
from typing import Any
from tools.git_agent import git_status

log = logging.getLogger(__name__)


def track_github_repository(repo_name: str = "Shreeprasandh/Luna") -> dict[str, Any]:
    """
    Inspects GitHub repository status, active branch, and modified files.

    Args:
        repo_name: GitHub repository owner/name (default 'Shreeprasandh/Luna').
    """
    log.info(f"[Tool: track_github_repository] Tracking repo '{repo_name}'...")
    g_res = git_status()
    return {
        "status": "success",
        "repository": repo_name,
        "branch": g_res.get("branch", "main"),
        "modified_files": g_res.get("modified_files_count", 0),
        "untracked_files": g_res.get("untracked_files_count", 0),
        "message": f"GitHub Repo '{repo_name}' active on branch '{g_res.get('branch', 'main')}'.",
    }
