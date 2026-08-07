"""
Environment Secret Vault Tool — Generates `.env.example` templates and inspects key configurations.
"""

import os
import logging
from typing import Any

log = logging.getLogger(__name__)

ENV_TEMPLATE = """# Luna Environment Secrets Template
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
LUNA_MASTER_PIN=100307
"""


def generate_env_vault_template(save_path: str = ".env.example") -> dict[str, Any]:
    """
    Generates a secure .env.example environment secret vault template file.
    """
    abs_path = os.path.abspath(save_path)
    log.info(f"[Tool: generate_env_vault_template] Writing secret template to '{abs_path}'...")
    try:
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(ENV_TEMPLATE)
        return {
            "status": "success",
            "template_path": abs_path,
            "message": f"Generated environment vault template at '{abs_path}'.",
        }
    except Exception as e:
        log.error(f"[Tool: generate_env_vault_template] Error: {e}")
        return {"status": "error", "message": f"Vault generation failed: {str(e)}"}
