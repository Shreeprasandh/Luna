"""
Network Diagnostic Tool — Checks local IP, ping latency, and internet connectivity.
"""

import socket
import subprocess
import logging
from typing import Any

log = logging.getLogger(__name__)


def get_network_diagnostics() -> dict[str, Any]:
    """
    Inspects network interfaces, local IP address, and tests ping latency to 8.8.8.8.
    """
    log.info("[Tool: get_network_diagnostics] Checking network connectivity...")
    try:
        # Get hostname and local IP
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        # Ping test to Google Public DNS
        ping_cmd = ["ping", "-n", "1", "8.8.8.8"] if socket.os.name == "nt" else ["ping", "-c", "1", "8.8.8.8"]
        ping_res = subprocess.run(ping_cmd, capture_output=True, text=True, timeout=3)

        online = ping_res.returncode == 0

        return {
            "status": "success",
            "hostname": hostname,
            "local_ip": local_ip,
            "internet_connected": online,
            "ping_output": ping_res.stdout.strip() if online else "Ping failed",
        }
    except Exception as e:
        log.error(f"[Tool: get_network_diagnostics] Error: {e}")
        return {
            "status": "error",
            "message": f"Network diagnostic failed: {str(e)}",
        }
