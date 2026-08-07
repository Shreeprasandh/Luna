"""
File System Tools — Safe file inspection, creation, and listing on local machine.
"""

import os
import logging
from typing import Any

log = logging.getLogger(__name__)


def read_file(filepath: str, max_lines: int = 300) -> dict[str, Any]:
    """
    Reads the content of a local file safely.

    Args:
        filepath: Absolute or relative path to the file.
        max_lines: Maximum number of lines to read (default 300).

    Returns:
        Dict with status, filepath, content, and line count.
    """
    log.info(f"[Tool: read_file] Reading: '{filepath}'")
    abs_path = os.path.abspath(filepath)

    if not os.path.exists(abs_path):
        return {
            "status": "error",
            "message": f"File not found: {filepath}",
        }

    if not os.path.isfile(abs_path):
        return {
            "status": "error",
            "message": f"Path is a directory, not a file: {filepath}",
        }

    try:
        with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
            lines = [f.readline() for _ in range(max_lines)]
            content = "".join(lines)

        return {
            "status": "success",
            "filepath": abs_path,
            "content": content,
            "line_count": len(lines),
        }
    except Exception as e:
        log.error(f"[Tool: read_file] Error reading {filepath}: {e}")
        return {
            "status": "error",
            "message": f"Failed to read file: {str(e)}",
        }


def write_file(filepath: str, content: str) -> dict[str, Any]:
    """
    Writes or overwrites a file on the local file system.
    Creates parent directories automatically if needed.

    Args:
        filepath: Path to the target file.
        content: Text content to write.

    Returns:
        Dict with status, filepath, and bytes written.
    """
    log.info(f"[Tool: write_file] Writing to: '{filepath}'")
    abs_path = os.path.abspath(filepath)

    try:
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "status": "success",
            "filepath": abs_path,
            "bytes_written": len(content.encode("utf-8")),
        }
    except Exception as e:
        log.error(f"[Tool: write_file] Error writing to {filepath}: {e}")
        return {
            "status": "error",
            "message": f"Failed to write file: {str(e)}",
        }


def list_directory(dirpath: str = ".") -> dict[str, Any]:
    """
    Lists the files and subdirectories inside a directory.

    Args:
        dirpath: Target directory path (defaults to current directory).

    Returns:
        Dict with status, dirpath, items (name, is_dir, size_bytes).
    """
    log.info(f"[Tool: list_directory] Listing: '{dirpath}'")
    abs_path = os.path.abspath(dirpath)

    if not os.path.exists(abs_path):
        return {
            "status": "error",
            "message": f"Directory not found: {dirpath}",
        }

    if not os.path.isdir(abs_path):
        return {
            "status": "error",
            "message": f"Path is a file, not a directory: {dirpath}",
        }

    try:
        items = []
        for entry in os.scandir(abs_path):
            items.append({
                "name": entry.name,
                "is_dir": entry.is_dir(),
                "size_bytes": entry.stat().st_size if not entry.is_dir() else None,
            })

        # Sort directories first, then files alphabetically
        items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))

        return {
            "status": "success",
            "dirpath": abs_path,
            "item_count": len(items),
            "items": items,
        }
    except Exception as e:
        log.error(f"[Tool: list_directory] Error listing {dirpath}: {e}")
        return {
            "status": "error",
            "message": f"Failed to list directory: {str(e)}",
        }
