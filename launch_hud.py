"""
Luna Floating Glassmorphic Desktop HUD Launcher.
Launches a sleek floating sidepanel desktop overlay.
"""

import sys
import os
import webbrowser
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def launch_desktop_hud():
    log.info("Launching Luna Glassmorphic Desktop HUD Overlay...")
    hud_url = "http://localhost:3000"
    webbrowser.open(hud_url)
    print(f"Luna HUD Active at: {hud_url}")


if __name__ == "__main__":
    launch_desktop_hud()
