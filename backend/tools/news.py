"""
Autonomous Tech News & Hacker News Digest Tool.
"""

import httpx
import logging
from typing import Any

log = logging.getLogger(__name__)


def get_tech_news_digest(topic: str = "technology") -> dict[str, Any]:
    """
    Fetches top tech news headlines from Hacker News API.
    """
    log.info("[Tool: get_tech_news_digest] Fetching top tech news headlines...")
    try:
        r = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=5.0)
        if r.status_code == 200:
            top_ids = r.json()[:5]
            stories = []
            for item_id in top_ids:
                item_res = httpx.get(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json", timeout=3.0)
                if item_res.status_code == 200:
                    data = item_res.json()
                    stories.append({
                        "title": data.get("title"),
                        "url": data.get("url"),
                        "score": data.get("score"),
                    })

            return {
                "status": "success",
                "count": len(stories),
                "stories": stories,
                "message": f"Fetched top {len(stories)} tech news headlines.",
            }

        return {"status": "error", "message": "Failed to reach Hacker News API"}
    except Exception as e:
        log.error(f"[Tool: get_tech_news_digest] Error: {e}")
        return {"status": "error", "message": f"News digest fetch failed: {str(e)}"}
