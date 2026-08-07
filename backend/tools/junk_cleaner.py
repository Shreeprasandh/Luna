"""
Disk Space Leak Analyzer & Junk File Cleaner Tool.
"""

import os
import logging
from typing import Any

log = logging.getLogger(__name__)


def clean_junk_files(dirpath: str = ".") -> dict[str, Any]:
    """
    Scans and removes temporary cache files and .tmp files to free up disk storage space.
    """
    abs_path = os.path.abspath(dirpath)
    log.info(f"[Tool: clean_junk_files] Scanning for junk files in '{abs_path}'...")
    removed_count = 0
    freed_bytes = 0

    try:
        for root, _, files in os.walk(abs_path):
            for file in files:
                if file.endswith((".tmp", ".log.old", ".bak", ".pyc")):
                    f_path = os.path.join(root, file)
                    try:
                        sz = os.path.getsize(f_path)
                        os.remove(f_path)
                        removed_count += 1
                        freed_bytes += sz
                    except Exception:
                        continue

        freed_mb = round(freed_bytes / (1024 * 1024), 2)
        return {
            "status": "success",
            "removed_files_count": removed_count,
            "freed_mb": freed_mb,
            "message": f"Cleaned {removed_count} temporary files ({freed_mb} MB disk space freed).",
        }
    except Exception as e:
        log.error(f"[Tool: clean_junk_files] Error: {e}")
        return {"status": "error", "message": f"Junk cleaning failed: {str(e)}"}
