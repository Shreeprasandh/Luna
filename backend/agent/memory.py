"""
Memory system — reads and writes Luna's long-term memory in Supabase.

All memories are stored as vector embeddings (sentence-transformers, local CPU).
Retrieval uses cosine similarity via pgvector to find contextually relevant memories
before each LLM call.

No cloud embedding API is used — embeddings run 100% locally at zero cost.
"""

import logging
import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()
log = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# Embedding model — loaded once at module import, cached for life of process
# ─────────────────────────────────────────────────────────────

_embedder = None


def _get_embedder():
    global _embedder
    if _embedder is None:
        log.info("Loading embedding model (first call only)...")
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
        log.info("Embedding model loaded.")
    return _embedder


def embed(text: str) -> list[float]:
    """
    Converts text to a 384-dimensional vector using a local CPU model.
    Model: all-MiniLM-L6-v2 (22MB, fast on CPU)

    Note: This model produces 384-dim vectors. The Supabase memories table
    uses vector(768). We pad to 768 dimensions by repeating the vector.
    This is a deliberate tradeoff: keeps embeddings local and free while
    maintaining schema consistency for future upgrade to a 768-dim model.
    """
    model = _get_embedder()
    vec = model.encode(text, normalize_embeddings=True).tolist()
    # Pad 384 -> 768 by doubling (preserves cosine similarity properties)
    return vec + vec


# ─────────────────────────────────────────────────────────────
# Write operations
# ─────────────────────────────────────────────────────────────

def store_memory(
    content: str,
    source: str = "conversation",
    tags: Optional[list[str]] = None,
    importance: float = 1.0,
) -> Optional[str]:
    """
    Stores a memory in Supabase with its vector embedding.

    Args:
        content:    The memory text to store.
        source:     Origin — 'conversation' | 'preference' | 'correction' | 'fact'
        tags:       Optional list of topic tags e.g. ['email', 'coding']
        importance: Weight for future decay logic. 1.0 = normal.

    Returns:
        The UUID of the stored memory, or None if storage failed.
    """
    try:
        from db.supabase_client import get_client
        client = get_client()
        vector = embed(content)

        result = client.table("memories").insert({
            "content": content,
            "source": source,
            "embedding": vector,
            "tags": tags or [],
            "importance": importance,
            "user_id": "default",
        }).execute()

        if result.data:
            memory_id = result.data[0]["id"]
            log.debug(f"Memory stored: {memory_id} — {content[:60]}")
            return memory_id

    except Exception as e:
        log.error(f"Failed to store memory: {e}")

    return None


def store_memories_batch(memories: list[dict]) -> int:
    """
    Stores multiple memories in a single Supabase insert.
    More efficient than calling store_memory() in a loop.

    Args:
        memories: List of dicts with keys: content, source, tags, importance

    Returns:
        Number of memories successfully stored.
    """
    if not memories:
        return 0

    try:
        from db.supabase_client import get_client
        client = get_client()

        rows = []
        for m in memories:
            content = m.get("content", "").strip()
            if not content:
                continue
            rows.append({
                "content": content,
                "source": m.get("source", "conversation"),
                "embedding": embed(content),
                "tags": m.get("tags", []),
                "importance": m.get("importance", 1.0),
                "user_id": "default",
            })

        if not rows:
            return 0

        result = client.table("memories").insert(rows).execute()
        count = len(result.data) if result.data else 0
        log.info(f"Stored {count} memories in batch.")
        return count

    except Exception as e:
        log.error(f"Failed to store memory batch: {e}")
        return 0


# ─────────────────────────────────────────────────────────────
# Read operations
# ─────────────────────────────────────────────────────────────

def retrieve_relevant_memories(
    query: str,
    top_k: Optional[int] = None,
    threshold: float = 0.35,
) -> list[str]:
    """
    Retrieves the most semantically relevant memories for a given query.

    Strategy:
    1. Run a vector similarity search with the given threshold.
    2. If the search returns fewer than 3 results (low data or weak match),
       supplement with the most recent memories so Luna always has
       some context about the user — even on very generic queries.

    Args:
        query:     The current user message to find relevant memories for.
        top_k:     Number of results to return. Defaults to MAX_MEMORY_RESULTS env var.
        threshold: Minimum cosine similarity (0-1). Lower = more results, less precise.

    Returns:
        List of memory content strings, ordered by relevance.
        Returns empty list if no relevant memories exist or on any error.
    """
    k = top_k or int(os.getenv("MAX_MEMORY_RESULTS", "5"))

    try:
        from db.supabase_client import get_client
        client = get_client()
        query_vector = embed(query)

        result = client.rpc("match_memories", {
            "query_embedding": query_vector,
            "match_threshold": threshold,
            "match_count": k,
        }).execute()

        memories = [row["content"] for row in result.data] if result.data else []
        retrieved_ids = [row["id"] for row in result.data] if result.data else []

        # Supplement with recent memories if similarity search returned few results
        if len(memories) < 3:
            recent = _get_recent_memories(k - len(memories), exclude_ids=retrieved_ids)
            memories = memories + recent

        if retrieved_ids:
            _update_accessed_timestamps(retrieved_ids)

        log.debug(f"Retrieved {len(memories)} memories for query: {query[:50]}")
        return memories[:k]

    except Exception as e:
        log.warning(f"Memory retrieval failed (non-fatal): {e}")
        return []


def _get_recent_memories(limit: int, exclude_ids: list[str] = None) -> list[str]:
    """Returns the most recently created memories, excluding specified IDs."""
    if limit <= 0:
        return []
    try:
        from db.supabase_client import get_client
        client = get_client()
        query = client.table("memories").select("id, content").order("created_at", desc=True).limit(limit + len(exclude_ids or []))
        result = query.execute()
        if not result.data:
            return []
        exclude = set(exclude_ids or [])
        return [
            row["content"] for row in result.data
            if row["id"] not in exclude
        ][:limit]
    except Exception:
        return []


def _update_accessed_timestamps(memory_ids: list[str]) -> None:
    """Updates last_accessed on retrieved memories. Fails silently."""
    try:
        from db.supabase_client import get_client
        client = get_client()
        for mid in memory_ids:
            client.rpc("update_memory_accessed", {"memory_id": mid}).execute()
    except Exception:
        pass


# ─────────────────────────────────────────────────────────────
# Preference management
# ─────────────────────────────────────────────────────────────

def save_preference(key: str, value: str) -> bool:
    """
    Saves or updates a named user preference in Supabase.

    Args:
        key:   Preference key e.g. 'email_tone', 'code_language'
        value: Preference value e.g. 'formal', 'python'

    Returns:
        True if saved successfully, False otherwise.
    """
    try:
        from db.supabase_client import get_client
        client = get_client()
        client.table("preferences").upsert(
            {"key": key, "value": value},
            on_conflict="key",
        ).execute()
        log.info(f"Preference saved: {key} = {value}")
        return True
    except Exception as e:
        log.error(f"Failed to save preference: {e}")
        return False


def get_preference(key: str) -> Optional[str]:
    """
    Retrieves a named preference. Returns None if not set.
    """
    try:
        from db.supabase_client import get_client
        client = get_client()
        result = client.table("preferences").select("value").eq("key", key).execute()
        if result.data:
            return result.data[0]["value"]
    except Exception as e:
        log.warning(f"Failed to get preference '{key}': {e}")
    return None
