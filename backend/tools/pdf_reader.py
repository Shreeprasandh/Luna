"""
PDF & Document Reader Tool — Reads and extracts text content from local PDF files.
"""

import os
import logging
from typing import Any
from pypdf import PdfReader

log = logging.getLogger(__name__)


def read_pdf_file(filepath: str, max_pages: int = 10) -> dict[str, Any]:
    """
    Reads text content from a local PDF file up to max_pages.

    Args:
        filepath: File path to local PDF document.
        max_pages: Maximum number of pages to extract (default 10).

    Returns:
        Dict with status, page count, and extracted text.
    """
    abs_path = os.path.abspath(filepath)
    log.info(f"[Tool: read_pdf_file] Reading PDF at '{abs_path}' (max_pages={max_pages})...")

    if not os.path.exists(abs_path):
        return {"status": "error", "message": f"PDF file not found: '{abs_path}'"}

    try:
        reader = PdfReader(abs_path)
        total_pages = len(reader.pages)
        pages_to_read = min(total_pages, max_pages)

        extracted_text = []
        for idx in range(pages_to_read):
            text = reader.pages[idx].extract_text() or ""
            extracted_text.append(f"--- Page {idx + 1} ---\n{text.strip()}")

        full_content = "\n\n".join(extracted_text)

        return {
            "status": "success",
            "filepath": abs_path,
            "total_pages": total_pages,
            "pages_read": pages_to_read,
            "content": full_content,
        }
    except Exception as e:
        log.error(f"[Tool: read_pdf_file] Error reading PDF '{abs_path}': {e}")
        return {
            "status": "error",
            "message": f"Failed to read PDF file: {str(e)}",
        }
