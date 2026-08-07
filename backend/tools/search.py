"""
Search Tools — Web search & Image search via DDGS.
100% free, zero API key, no quota limits.
"""

import logging
from typing import Any
from ddgs import DDGS

log = logging.getLogger(__name__)


def web_search(query: str, max_results: int = 4) -> dict[str, Any]:
    """
    Performs a web search for a given text query.

    Args:
        query: The search term or topic to look up.
        max_results: Number of results to return (default 4).

    Returns:
        Dict containing query and list of result dicts (title, snippet, url).
    """
    log.info(f"[Tool: web_search] Query: '{query}'")
    try:
        results = []
        with DDGS() as ddgs:
            raw_results = list(ddgs.text(query, max_results=max_results))
            for r in raw_results:
                results.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "url": r.get("href", ""),
                })
        return {
            "status": "success",
            "query": query,
            "results": results,
        }
    except Exception as e:
        log.error(f"[Tool: web_search] Error: {e}")
        return {
            "status": "error",
            "query": query,
            "message": f"Web search failed: {str(e)}",
            "results": [],
        }


def image_search(query: str, max_results: int = 3) -> dict[str, Any]:
    """
    Performs an image search to find visual results for rendering in the panel.

    Args:
        query: The visual topic or image query.
        max_results: Number of image results (default 3).

    Returns:
        Dict containing query and list of image dicts (title, image_url, thumbnail).
    """
    log.info(f"[Tool: image_search] Query: '{query}'")
    try:
        results = []
        with DDGS() as ddgs:
            raw_results = list(ddgs.images(query, max_results=max_results))
            for r in raw_results:
                results.append({
                    "title": r.get("title", ""),
                    "image_url": r.get("image", ""),
                    "thumbnail": r.get("thumbnail", ""),
                    "source": r.get("url", ""),
                })
        return {
            "status": "success",
            "query": query,
            "images": results,
        }
    except Exception as e:
        log.error(f"[Tool: image_search] Error: {e}")
        return {
            "status": "error",
            "query": query,
            "message": f"Image search failed: {str(e)}",
            "images": [],
        }
