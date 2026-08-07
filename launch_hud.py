"""
Luna Floating Glassmorphic Desktop HUD Launcher.
Launches a frameless floating sidepanel window on Windows desktop.
"""

import sys
import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def launch_desktop_hud():
    log.info("Launching Luna Glassmorphic Desktop HUD Overlay Window...")
    hud_url = "http://localhost:3000"

    # Try PyWebView first for frameless glass window
    try:
        import webview
        log.info("Starting PyWebView frameless glass window...")
        window = webview.create_window(
            title="Luna Assistant",
            url=hud_url,
            width=440,
            height=720,
            x=1440,
            y=150,
            resizable=True,
            frameless=False,
            easy_drag=True,
            on_top=True
        )
        webview.start()
        return
    except Exception as e:
        log.info(f"PyWebView not available ({e}), falling back to Chrome App Mode...")

    # Fallback to Chrome Application Mode
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]

    chrome_bin = None
    for path in chrome_paths:
        if os.path.exists(path):
            chrome_bin = path
            break

    if chrome_bin:
        cmd = [
            chrome_bin,
            f"--app={hud_url}",
            "--window-size=440,750",
            "--window-position=1440,150",
            "--disable-http-cache"
        ]
        subprocess.Popen(cmd)
        log.info(f"Luna Floating HUD launched via '{os.path.basename(chrome_bin)}' App Mode!")
    else:
        import webbrowser
        webbrowser.open(hud_url)


if __name__ == "__main__":
    launch_desktop_hud()
