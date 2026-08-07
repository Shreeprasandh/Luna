"""
Google Drive & Cloud Storage Sync Bridge Tool.
"""

import os
import shutil
import logging
from typing import Any

log = logging.getLogger(__name__)


def sync_cloud_file(filepath: str, destination_folder: str = "CloudDrive") -> dict[str, Any]:
    """
    Syncs a local file to the local Cloud Drive sync folder.
    """
    abs_src = os.path.abspath(filepath)
    abs_dest_dir = os.path.abspath(destination_folder)
    os.makedirs(abs_dest_dir, exist_ok=True)

    if not os.path.exists(abs_src):
        return {"status": "error", "message": f"Source file not found: '{filepath}'"}

    filename = os.path.basename(abs_src)
    dest_path = os.path.join(abs_dest_dir, filename)

    log.info(f"[Tool: sync_cloud_file] Syncing '{abs_src}' -> '{dest_path}'...")
    try:
        shutil.copy2(abs_src, dest_path)
        return {
            "status": "success",
            "source": abs_src,
            "destination": dest_path,
            "message": f"Synced '{filename}' to Cloud Drive folder '{destination_folder}'.",
        }
    except Exception as e:
        log.error(f"[Tool: sync_cloud_file] Error: {e}")
        return {"status": "error", "message": f"Cloud sync failed: {str(e)}"}
