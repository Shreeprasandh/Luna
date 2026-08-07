"""
Security & Active Port Inspector Tool — Scans active listening network ports and connections.
"""

import logging
from typing import Any
import psutil

log = logging.getLogger(__name__)


def get_open_ports() -> dict[str, Any]:
    """
    Scans active listening network ports and connections on the machine to detect open services.
    """
    log.info("[Tool: get_open_ports] Scanning open network listening ports...")
    try:
        listening_ports = []
        for conn in psutil.net_connections(kind="inet"):
            if conn.status == psutil.CONN_LISTEN:
                try:
                    proc = psutil.Process(conn.pid) if conn.pid else None
                    proc_name = proc.name() if proc else "Unknown"
                except Exception:
                    proc_name = "System"

                listening_ports.append({
                    "port": conn.laddr.port,
                    "ip": conn.laddr.ip,
                    "pid": conn.pid,
                    "process": proc_name,
                })

        return {
            "status": "success",
            "open_port_count": len(listening_ports),
            "ports": listening_ports[:20],
        }
    except Exception as e:
        log.error(f"[Tool: get_open_ports] Error: {e}")
        return {"status": "error", "message": f"Port scan failed: {str(e)}"}
