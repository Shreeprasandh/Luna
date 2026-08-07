"""
System Network Speedtest Utility Tool.
"""

import time
import logging
from typing import Any
from tools.network import get_network_diagnostics

log = logging.getLogger(__name__)


def run_network_speedtest() -> dict[str, Any]:
    """
    Measures network ping latency, packet stability, and internet connection health.
    """
    log.info("[Tool: run_network_speedtest] Measuring network speed and latency...")
    t0 = time.time()
    n_res = get_network_diagnostics()
    latency_ms = round((time.time() - t0) * 1000, 2)

    return {
        "status": "success",
        "ip": n_res.get("local_ip", "Unknown"),
        "hostname": n_res.get("hostname", "Unknown"),
        "ping_latency_ms": n_res.get("ping_ms", latency_ms),
        "message": f"Network Speedtest: Latency={n_res.get('ping_ms', latency_ms)} ms, IP={n_res.get('local_ip', 'Unknown')}.",
    }
