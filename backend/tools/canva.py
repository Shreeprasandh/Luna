"""
Canva Design & Invitation Creator Tool — Opens Canva design templates directly for editing.
"""

import urllib.parse
import webbrowser
import logging
from typing import Any

log = logging.getLogger(__name__)


def open_canva_design(design_type: str = "invitation", topic: str = "birthday party") -> dict[str, Any]:
    """
    Opens Canva design canvas pre-configured for a specified template (e.g. invitation, poster, presentation, thumbnail).

    Args:
        design_type: Type of design ('invitation', 'poster', 'presentation', 'logo', 'thumbnail').
        topic: Specific theme or topic (e.g. 'wedding party', 'hackathon poster', 'AI presentation').
    """
    query = f"{design_type} {topic}".strip()
    encoded = urllib.parse.quote(query)
    canva_url = f"https://www.canva.com/search?q={encoded}"

    log.info(f"[Tool: open_canva_design] Opening Canva for '{query}'...")
    try:
        webbrowser.open(canva_url)
        return {
            "status": "success",
            "design_type": design_type,
            "topic": topic,
            "canva_url": canva_url,
            "message": f"Opened Canva template editor for '{query}'.",
        }
    except Exception as e:
        log.error(f"[Tool: open_canva_design] Error: {e}")
        return {"status": "error", "message": f"Failed to open Canva design: {str(e)}"}
