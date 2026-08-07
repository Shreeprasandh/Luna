"""
Automated File Organizer & Disk Cleaner Tool — Sorts messy directories and identifies large junk files.
"""

import os
import shutil
import logging
from typing import Any

log = logging.getLogger(__name__)

CATEGORY_MAP = {
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico"],
    "Code": [".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".html", ".css", ".sql"],
    "Archives": [".zip", ".tar", ".gz", ".7z", ".rar"],
    "Executables": [".exe", ".msi", ".bat", ".ps1"],
}


def organize_directory(dirpath: str = ".") -> dict[str, Any]:
    """
    Sorts files in a directory into categorized subfolders (Documents, Images, Code, Archives, Executables).

    Args:
        dirpath: Target folder path to organize.

    Returns:
        Dict with status, organized_count, and category statistics.
    """
    abs_path = os.path.abspath(dirpath)
    log.info(f"[Tool: organize_directory] Organizing folder '{abs_path}'...")

    if not os.path.exists(abs_path):
        return {"status": "error", "message": f"Directory not found: '{abs_path}'"}

    moved_count = 0
    stats = {cat: 0 for cat in CATEGORY_MAP}

    try:
        for filename in os.listdir(abs_path):
            file_path = os.path.join(abs_path, filename)
            if os.path.isfile(file_path):
                ext = os.path.splitext(filename)[1].lower()
                for category, extensions in CATEGORY_MAP.items():
                    if ext in extensions:
                        dest_dir = os.path.join(abs_path, category)
                        os.makedirs(dest_dir, exist_ok=True)
                        shutil.move(file_path, os.path.join(dest_dir, filename))
                        moved_count += 1
                        stats[category] += 1
                        break

        return {
            "status": "success",
            "directory": abs_path,
            "organized_count": moved_count,
            "categories": stats,
            "message": f"Organized {moved_count} files in {abs_path}.",
        }
    except Exception as e:
        log.error(f"[Tool: organize_directory] Error: {e}")
        return {"status": "error", "message": f"Organization failed: {str(e)}"}


def find_large_files(dirpath: str = ".", min_size_mb: int = 100) -> dict[str, Any]:
    """
    Finds files larger than min_size_mb taking up space on disk.

    Args:
        dirpath: Starting search directory.
        min_size_mb: Minimum file size in MB to flag (default 100MB).
    """
    abs_path = os.path.abspath(dirpath)
    min_bytes = min_size_mb * 1024 * 1024
    log.info(f"[Tool: find_large_files] Searching for files > {min_size_mb}MB in '{abs_path}'...")

    large_files = []
    try:
        for root, dirs, files in os.walk(abs_path):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "venv", "__pycache__")]
            for f in files:
                filepath = os.path.join(root, f)
                try:
                    size = os.path.getsize(filepath)
                    if size >= min_bytes:
                        large_files.append({
                            "filepath": filepath,
                            "size_mb": round(size / (1024 * 1024), 2),
                        })
                except Exception:
                    continue
                if len(large_files) >= 20:
                    break
            if len(large_files) >= 20:
                break

        return {
            "status": "success",
            "dirpath": abs_path,
            "min_size_mb": min_size_mb,
            "found_count": len(large_files),
            "files": large_files,
        }
    except Exception as e:
        log.error(f"[Tool: find_large_files] Error: {e}")
        return {"status": "error", "message": f"Large file scan failed: {str(e)}"}
