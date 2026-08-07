"""
Luna One-Command Boot Switch (Local Environment)
Initialises backend server and voice daemon in synchronized subprocesses.

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
VENV_PYTHON = os.path.join(BACKEND_DIR, "venv", "Scripts", "python.exe")


def check_prerequisites():
    """Verifies python environment and .env configuration."""
    if not os.path.exists(VENV_PYTHON):
        log.error(f"Virtual environment python not found at: {VENV_PYTHON}")
        log.error("Please run environment setup first.")
        sys.exit(1)

    env_path = os.path.join(BACKEND_DIR, ".env")
    if not os.path.exists(env_path):
        log.error(f"Environment file missing: {env_path}")
        sys.exit(1)

    log.info("Prerequisites verified.")


def boot():
    """Boots Luna backend and daemon processes."""
    check_prerequisites()

    log.info("==========================================")
    log.info("        BOOTING LUNA SYSTEM               ")
    log.info("==========================================")

    # 1. Start FastAPI Backend
    log.info("Starting Backend Server (port 8000)...")
    backend_cmd = [VENV_PYTHON, "-m", "uvicorn", "main:app", "--port", "8000"]
    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=BACKEND_DIR,
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0,
    )
    time.sleep(3)

    # 2. Start Voice Daemon
    log.info("Starting Desktop Voice Daemon...")
    daemon_cmd = [VENV_PYTHON, "main.py"]
    daemon_proc = subprocess.Popen(
        daemon_cmd,
        cwd=DAEMON_DIR,
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0,
    )

    log.info("Luna System Online.")
    log.info("To stop all processes, run: python kill_luna.py")

    try:
        backend_proc.wait()
        daemon_proc.wait()
    except KeyboardInterrupt:
        log.info("Boot process interrupted. Shutting down...")
        backend_proc.terminate()
        daemon_proc.terminate()


if __name__ == "__main__":
    boot()
