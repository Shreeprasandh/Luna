"""
Wi-Fi Device Intrusion Scanner Tool — Scans local network ARP table to inspect connected IP addresses.
"""

import subprocess
import logging
from typing import Any

log = logging.getLogger(__name__)


def scan_wifi_devices() -> dict[str, Any]:
    """
    Scans local Wi-Fi network ARP table to inspect connected IP addresses and MAC addresses.
    """
    log.info("[Tool: scan_wifi_devices] Scanning local network ARP table...")
    try:
        res = subprocess.run(["arp", "-a"], capture_output=True, text=True)
        lines = [line.strip() for line in res.stdout.splitlines() if line.strip() and "dynamic" in line.lower()]
        devices = []
        for line in lines[:15]:
            parts = line.split()
            if len(parts) >= 2:
                devices.append({"ip": parts[0], "mac": parts[1]})

        return {
            "status": "success",
            "device_count": len(devices),
            "devices": devices,
            "message": f"Scanned local network: {len(devices)} active Wi-Fi devices detected.",
        }
    except Exception as e:
        log.error(f"[Tool: scan_wifi_devices] Error: {e}")
        return {"status": "error", "message": f"Wi-Fi scan failed: {str(e)}"}
