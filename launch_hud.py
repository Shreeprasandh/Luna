"""
Luna Desktop Native HUD Window Launcher
Creates a lightweight, frameless desktop overlay window for Luna's Next.js sidepanel UI.

Usage:
  python launch_hud.py
"""

import sys
import webview

PANEL_URL = "http://localhost:3000"


def launch_hud():
    """Launches frameless sidepanel window positioned on right side of primary monitor."""
    print("==========================================")
    print("   LAUNCHING LUNA NATIVE DESKTOP HUD      ")
    print("==========================================")

    window = webview.create_window(
        title="Luna Assistant",
        url=PANEL_URL,
        width=440,
        height=860,
        resizable=True,
        frameless=False,
        easy_drag=True,
        on_top=True,
    )

    webview.start()


if __name__ == "__main__":
    launch_hud()
