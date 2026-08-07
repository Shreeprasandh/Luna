"""
Luna Local Kill Switch Process Manager
Safely terminates all local Luna processes (Backend, Next.js UI Panel, Desktop Daemon).

Usage:
  python kill_luna.py
"""

import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [KILL_SWITCH] %(message)s")
log = logging.getLogger("LunaKillSwitch")


def execute_cmd(cmd: str) -> str:
    try:
        res = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
        return res.stdout
    except Exception as e:
        log.error(f"Error executing command '{cmd}': {e}")
        return ""


def kill_luna_processes():
    """Finds and terminates all Luna backend, panel, and daemon processes."""
    log.info("==========================================")
    log.info("    EXECUTING LUNA KILL SWITCH            ")
    log.info("==========================================")

    # 1. Kill process on Port 8000 (Backend) and Port 3000 (Next.js Panel)
    cmd_port = """
    foreach ($port in @(8000, 3000)) {
        $conn = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
        if ($conn) {
            $conn | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
            Write-Host "Port $port process terminated."
        } else {
            Write-Host "Port $port is clean."
        }
    }
    """
    out_port = execute_cmd(cmd_port)
    log.info(out_port.strip())

    # 2. Kill lingering uvicorn, python, or node dev processes
    cmd_proc = """
    Get-Process -Name "uvicorn" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*main:app*" -or $_.CommandLine -like "*daemon*" -or $_.CommandLine -like "*launch_hud*" } | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "Luna python and background processes terminated."
    """
    out_proc = execute_cmd(cmd_proc)
    log.info(out_proc.strip())

    log.info("Kill Switch Execution Complete. All Luna processes stopped.")


if __name__ == "__main__":
    kill_luna_processes()
