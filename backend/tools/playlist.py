"""
Smart Playlist Generator Tool — Generates mood-based Spotify/YouTube music playlists.
"""

import logging
from typing import Any
from tools.media import play_spotify_song

log = logging.getLogger(__name__)

MOOD_QUERIES = {
    "focus": "lofi deep focus study beats",
    "coding": "synthwave cyberpunk coding music",
    "chill": "acoustic chill relax instrumental",
    "workout": "high energy motivation electronic",
}


def generate_smart_playlist(mood: str = "focus") -> dict[str, Any]:
    """
    Generates and plays a music playlist tailored to your mood ('focus', 'coding', 'chill', 'workout').
    """
    clean_mood = mood.strip().lower()
    query = MOOD_QUERIES.get(clean_mood, f"{clean_mood} music playlist")
    log.info(f"[Tool: generate_smart_playlist] Generating '{clean_mood}' playlist...")

    return play_spotify_song(query)
