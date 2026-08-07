"""
System Hardware & PC Health Monitor Tool — Inspects CPU, RAM, Disk, and Process metrics.
Allows Luna to monitor PC performance and identify resource bottlenecks.
"""

import logging
from typing import Any
import psutil

log = logging.getLogger(__name__)


def get_system_health() -> dict[str, Any]:
    """
    Returns real-time system hardware metrics including CPU, RAM, Disk usage, and top processes.
    """
    log.info("[Tool: get_system_health] Gathering PC hardware metrics...")
    try:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        # Top 3 CPU-consuming processes
        processes = []
        for proc in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
                           key=lambda p: p.info.get('cpu_percent') or 0,
                           reverse=True)[:3]:
            processes.append({
                "name": proc.info.get("name"),
                "pid": proc.info.get("pid"),
                "cpu_percent": proc.info.get("cpu_percent"),
                "ram_percent": round(proc.info.get("memory_percent") or 0, 1),
            })

        return {
            "status": "success",
            "cpu": {
                "usage_percent": cpu_percent,
                "core_count": psutil.cpu_count(logical=True),
            },
            "ram": {
                "used_gb": round(memory.used / (1024**3), 2),
                "total_gb": round(memory.total / (1024**3), 2),
                "usage_percent": memory.percent,
            },
            "disk": {
                "used_gb": round(disk.used / (1024**3), 2),
                "total_gb": round(disk.total / (1024**3), 2),
                "usage_percent": disk.percent,
            },
            "top_processes": processes,
        }
    except Exception as e:
        log.error(f"[Tool: get_system_health] Error: {e}")
        return {
            "status": "error",
            "message": f"Failed to inspect system health: {str(e)}",
        }
