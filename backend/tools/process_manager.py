"""
Process Manager & Kill Switch Tool — Inspects and terminates high-memory background processes.
"""

import logging
from typing import Any
import psutil

log = logging.getLogger(__name__)


def list_top_processes(limit: int = 10) -> dict[str, Any]:
    """
    Lists top background processes consuming CPU and memory.
    """
    try:
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                procs.append(p.info)
            except Exception:
                continue

        procs.sort(key=lambda x: x.get('memory_percent') or 0, reverse=True)
        return {
            "status": "success",
            "count": len(procs[:limit]),
            "processes": procs[:limit],
        }
    except Exception as e:
        log.error(f"[Tool: list_top_processes] Error: {e}")
        return {"status": "error", "message": f"Process scan failed: {str(e)}"}


def terminate_process_by_name(process_name: str) -> dict[str, Any]:
    """
    Terminates background process by executable name (e.g. 'notepad.exe', 'calculator.exe').
    """
    clean_name = process_name.strip().lower()
    terminated_count = 0

    try:
        for p in psutil.process_iter(['pid', 'name']):
            try:
                if p.info['name'] and p.info['name'].lower() == clean_name:
                    p.terminate()
                    terminated_count += 1
            except Exception:
                continue

        return {
            "status": "success",
            "process_name": clean_name,
            "terminated_count": terminated_count,
            "message": f"Terminated {terminated_count} instances of '{clean_name}'.",
        }
    except Exception as e:
        log.error(f"[Tool: terminate_process_by_name] Error: {e}")
        return {"status": "error", "message": f"Termination failed: {str(e)}"}
