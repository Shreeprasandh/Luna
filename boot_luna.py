"""
Luna One-Command Boot Switch (Full System Stack)
Initialises backend server, Next.js UI panel, voice daemon, and floating desktop HUD orb.

Usage:
  python boot_luna.py
"""

import os
import sys
import time
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [BOOT] %(message)s")
log = logging.getLogger("LunaBoot")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
DAEMON_DIR = os.path.join(ROOT_DIR, "daemon")
PANEL_DIR = os.path.join(ROOT_DIR, "panel")
VENV_PYTHON = os.path.join(BACKEND_DIR, "venv", "Scripts", "python.exe")


def check_prerequisites():
    """Verifies python environment and .env configuration."""
    if not os.path.exists(VENV_PYTHON):
        log.error(f"Virtual environment python not found at: {VENV_PYTHON}")
        sys.exit(1)

    env_path = os.path.join(BACKEND_DIR, ".env")
    if not os.path.exists(env_path):
        log.error(f"Environment file missing: {env_path}")
        sys.exit(1)

    log.info("Prerequisites verified.")


def boot():
    """Boots Luna backend, Next.js panel, daemon, and HUD window."""
    check_prerequisites()

    log.info("==========================================")
    log.info("        BOOTING LUNA SYSTEM STACK         ")
    log.info("==========================================")

    # 1. Start FastAPI Backend
    log.info("1/4 Starting Backend Server (http://localhost:8000)...")
    backend_cmd = [VENV_PYTHON, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=BACKEND_DIR,
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0,
    )
    time.sleep(2)

    # 2. Start Next.js Panel UI
    log.info("2/4 Starting Next.js Desktop Panel (http://localhost:3000)...")
    panel_cmd = ["npm.cmd" if os.name == "nt" else "npm", "run", "dev"]
    panel_proc = subprocess.Popen(
        panel_cmd,
        cwd=PANEL_DIR,
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0,
    )
    time.sleep(2)

    # 3. Start Desktop Voice Daemon
    log.info("3/4 Starting Desktop Voice Daemon...")
    daemon_cmd = [VENV_PYTHON, "main.py"]
    daemon_proc = subprocess.Popen(
        daemon_cmd,
        cwd=DAEMON_DIR,
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0,
    )
    time.sleep(1)

    # 4. Launch Desktop Floating HUD Orb Window
    log.info("4/4 Launching Floating Desktop HUD Orb Window...")
    hud_cmd = [VENV_PYTHON, "launch_hud.py"]
    hud_proc = subprocess.Popen(
        hud_cmd,
        cwd=ROOT_DIR,
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0,
    )

    log.info("==========================================")
    log.info(" Luna System Stack & HUD Orb Online.")
    log.info(" UI Panel:   http://localhost:3000")
    log.info(" Backend:    http://localhost:8000")
    log.info(" Stop All:   python kill_luna.py")
    log.info("==========================================")

    try:
        backend_proc.wait()
        panel_proc.wait()
        daemon_proc.wait()
        hud_proc.wait()
    except KeyboardInterrupt:
        log.info("Boot process interrupted. Shutting down...")
        backend_proc.terminate()
        panel_proc.terminate()
        daemon_proc.terminate()
        hud_proc.terminate()


if __name__ == "__main__":
    boot()
