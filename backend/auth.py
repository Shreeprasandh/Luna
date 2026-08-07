"""
Mobile Authentication & Hacker-Proof Guard — Protects mobile remote control endpoints with PIN authentication.
"""

import os
import logging
from dotenv import load_dotenv

load_dotenv()
log = logging.getLogger(__name__)

# Master access PIN for mobile remote authentication
DEFAULT_MASTER_PIN = os.getenv("LUNA_MASTER_PIN", "100307")


def verify_access_pin(provided_pin: str) -> bool:
    """
    Verifies if the provided mobile PIN matches the master secret PIN.
    """
    clean_pin = str(provided_pin).strip()
    is_valid = clean_pin == DEFAULT_MASTER_PIN
    if not is_valid:
        log.warning(f"SECURITY ALERT: Invalid mobile access PIN attempt: '{clean_pin}'")
    return is_valid
