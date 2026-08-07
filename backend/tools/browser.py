"""
Browser Automation Tool — Playwright headless browser for web scraping and page rendering.
Allows Luna to visit JavaScript-rendered websites, extract text content, and capture page screenshots.
"""

import os
import logging
from typing import Any
from playwright.sync_api import sync_playwright

log = logging.getLogger(__name__)


def browse_url(url: str, max_text_length: int = 2500) -> dict[str, Any]:
    """
    Navigates to a webpage using Playwright headless browser and extracts clean text content.

    Args:
        url: The web URL to visit.
        max_text_length: Maximum characters of text to return (default 2500).

    Returns:
        Dict containing status, url, page title, and extracted text.
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    log.info(f"[Tool: browse_url] Visiting URL: '{url}'")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=20000, wait_until="domcontentloaded")

            title = page.title()
            
            # Extract main readable text from body
            body_text = page.inner_text("body")
            cleaned_text = " ".join(body_text.split())[:max_text_length]

            browser.close()

            return {
                "status": "success",
                "url": url,
                "title": title,
                "text_content": cleaned_text,
            }

    except Exception as e:
        log.error(f"[Tool: browse_url] Error visiting {url}: {e}")
        return {
            "status": "error",
            "url": url,
            "message": f"Failed to browse URL: {str(e)}",
            "text_content": "",
        }


def take_screenshot(url: str, save_path: str = "design/page_preview.png") -> dict[str, Any]:
    """
    Captures a visual screenshot of a webpage and saves it locally.

    Args:
        url: The web URL to capture.
        save_path: Relative or absolute destination path for PNG file.

    Returns:
        Dict containing status, url, and destination filepath.
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    abs_save_path = os.path.abspath(save_path)
    os.makedirs(os.path.dirname(abs_save_path), exist_ok=True)

    log.info(f"[Tool: take_screenshot] Capturing '{url}' to '{abs_save_path}'")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            page.goto(url, timeout=20000, wait_until="domcontentloaded")

            page.screenshot(path=abs_save_path, full_page=False)
            title = page.title()
            browser.close()

            return {
                "status": "success",
                "url": url,
                "title": title,
                "filepath": abs_save_path,
            }

    except Exception as e:
        log.error(f"[Tool: take_screenshot] Error capturing {url}: {e}")
        return {
            "status": "error",
            "url": url,
            "message": f"Failed to capture screenshot: {str(e)}",
        }
