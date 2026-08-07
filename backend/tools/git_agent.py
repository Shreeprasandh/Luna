"""
Autonomous Git Agent Tool — Enables Luna to inspect repo status, commit changes, and push code.
"""

import os
import subprocess
import logging
from typing import Any

log = logging.getLogger(__name__)


def git_status(repo_path: str = ".") -> dict[str, Any]:
    """
    Returns current Git repository branch, modified files, and staging status.
    """
    abs_path = os.path.abspath(repo_path)
    log.info(f"[Tool: git_status] Inspecting repository at '{abs_path}'")

    try:
        branch_res = subprocess.run(["git", "branch", "--show-current"], cwd=abs_path, capture_output=True, text=True)
        status_res = subprocess.run(["git", "status", "--short"], cwd=abs_path, capture_output=True, text=True)

        branch = branch_res.stdout.strip()
        changes = status_res.stdout.strip().split("\n") if status_res.stdout.strip() else []

        return {
            "status": "success",
            "repo_path": abs_path,
            "branch": branch,
            "modified_files_count": len(changes),
            "changes": changes,
        }
    except Exception as e:
        log.error(f"[Tool: git_status] Error: {e}")
        return {
            "status": "error",
            "message": f"Failed to get git status: {str(e)}",
        }


def git_commit_and_push(commit_message: str, repo_path: str = ".") -> dict[str, Any]:
    """
    Stages all changes, creates a commit with the provided message, and pushes to origin.
    """
    abs_path = os.path.abspath(repo_path)
    log.info(f"[Tool: git_commit_and_push] Committing: '{commit_message}' in '{abs_path}'")

    try:
        subprocess.run(["git", "add", "."], cwd=abs_path, check=True)
        commit_res = subprocess.run(["git", "commit", "-m", commit_message], cwd=abs_path, capture_output=True, text=True)
        push_res = subprocess.run(["git", "push", "origin", "main"], cwd=abs_path, capture_output=True, text=True)

        return {
            "status": "success",
            "commit_message": commit_message,
            "commit_output": commit_res.stdout.strip(),
            "push_output": push_res.stdout.strip(),
        }
    except Exception as e:
        log.error(f"[Tool: git_commit_and_push] Error: {e}")
        return {
            "status": "error",
            "message": f"Git commit or push failed: {str(e)}",
        }
