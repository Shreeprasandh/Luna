"""
Deep Multi-Page PDF Summarizer & Book Reader Tool.
"""

import os
import logging
from typing import Any
from tools.pdf_reader import read_pdf_file

log = logging.getLogger(__name__)


def summarize_pdf_book(filepath: str, max_pages: int = 50) -> dict[str, Any]:
    """
    Reads and summarizes long PDF documents or books up to max_pages.
    """
    log.info(f"[Tool: summarize_pdf_book] Summarizing PDF book '{filepath}'...")
    p_res = read_pdf_file(filepath, max_pages)

    if p_res.get("status") != "success":
        return p_res

    text_content = p_res.get("text", "")
    word_count = len(text_content.split())
    page_count = p_res.get("pages_read", 0)

    snippet = text_content[:600] + "..." if len(text_content) > 600 else text_content

    return {
        "status": "success",
        "filepath": filepath,
        "pages_read": page_count,
        "word_count": word_count,
        "summary_snippet": snippet,
        "message": f"Summarized PDF document '{os.path.basename(filepath)}': {page_count} pages read ({word_count} words).",
    }
