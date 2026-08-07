"""
Spotify & Media Controller Tool — Plays songs on Spotify and fetches live song lyrics.
"""

import urllib.parse
import webbrowser
import logging
from typing import Any
from tools.search import web_search

log = logging.getLogger(__name__)


def play_spotify_song(song_name: str) -> dict[str, Any]:
    """
    Searches and plays a song or playlist on Spotify.

    Args:
        song_name: Song title or artist name to play.
    """
    clean_query = song_name.strip()
    encoded = urllib.parse.quote(clean_query)
    spotify_url = f"https://open.spotify.com/search/{encoded}"

    log.info(f"[Tool: play_spotify_song] Playing '{clean_query}' on Spotify...")
    try:
        webbrowser.open(spotify_url)
        return {
            "status": "success",
            "song": clean_query,
            "url": spotify_url,
            "message": f"Opened Spotify search and player for '{clean_query}'.",
        }
    except Exception as e:
        log.error(f"[Tool: play_spotify_song] Error: {e}")
        return {"status": "error", "message": f"Failed to play Spotify song: {str(e)}"}


def get_song_lyrics(song_title: str) -> dict[str, Any]:
    """
    Fetches the lyrics for a song by title and artist name.

    Args:
        song_title: Song title (e.g. 'Bohemian Rhapsody Queen').
    """
    clean_title = song_title.strip()
    log.info(f"[Tool: get_song_lyrics] Fetching lyrics for '{clean_title}'...")

    try:
        search_res = web_search(f"lyrics {clean_title}")
        if search_res.get("status") == "success":
            results = search_res.get("results", [])
            snippet = results[0]["snippet"] if results else "Lyrics search returned no text snippet."
            return {
                "status": "success",
                "song_title": clean_title,
                "lyrics_summary": snippet,
                "sources": results[:2],
            }
        return {"status": "error", "message": "Could not find lyrics."}
    except Exception as e:
        log.error(f"[Tool: get_song_lyrics] Error: {e}")
        return {"status": "error", "message": f"Failed to fetch lyrics: {str(e)}"}
