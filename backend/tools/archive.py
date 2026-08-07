"""
File Compressor & Archive Tool — Zips and extracts directory archives.
"""

import os
import shutil
import logging
from typing import Any

log = logging.getLogger(__name__)


def zip_directory(source_dir: str = ".", output_filename: str = "archive.zip") -> dict[str, Any]:
    """
    Compresses a directory into a .zip archive.

    Args:
        source_dir: Directory path to compress.
        output_filename: Output archive file name.
    """
    abs_src = os.path.abspath(source_dir)
    abs_out = os.path.abspath(output_filename)
    if abs_out.endswith(".zip"):
        abs_out = abs_out[:-4]

    log.info(f"[Tool: zip_directory] Zipping '{abs_src}' to '{abs_out}.zip'...")
    try:
        archive_path = shutil.make_archive(abs_out, "zip", abs_src)
        return {
            "status": "success",
            "source_dir": abs_src,
            "archive_path": archive_path,
            "message": f"Created ZIP archive at '{archive_path}'.",
        }
    except Exception as e:
        log.error(f"[Tool: zip_directory] Error: {e}")
        return {"status": "error", "message": f"Compression failed: {str(e)}"}
