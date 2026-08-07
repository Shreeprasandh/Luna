"""
Supabase client — single shared instance for the entire backend.
Uses the service_role key to bypass RLS for all operations.
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

_client: Client | None = None


def get_client() -> Client:
    """
    Returns the shared Supabase client.
    Initialised once on first call, reused for every subsequent call.
    """
    global _client

    if _client is not None:
        return _client

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not url or not key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in backend/.env"
        )

    _client = create_client(url, key)
    return _client
