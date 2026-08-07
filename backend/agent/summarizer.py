"""
Session Summarizer — extracts and stores memories at the end of each session.

Runs after a session ends. Sends the full conversation to the LLM with a
structured extraction prompt. The output is parsed and written to Supabase
as individual memory records with embeddings.

This is how Luna gets smarter over time — every conversation contributes
structured knowledge, not raw chat logs.
"""

import json
import logging

from agent.llm import chat
from agent.memory import store_memories_batch

log = logging.getLogger(__name__)

EXTRACTION_PROMPT = """You are a memory extraction system. Given a conversation between a user and Luna (an AI assistant), extract structured facts that should be remembered long-term.

Extract ONLY meaningful, durable information. Do not extract trivial exchanges.

Categories to extract:
1. facts       — stable facts about the user (name, location, relationships, projects)
2. preference  — how the user likes things done (tone, format, tools, style)
3. correction  — things the user corrected or said Luna got wrong
4. pattern     — recurring behaviours or habits observed

Output a JSON array only. No explanation, no markdown, just the array.

Format:
[
  {
    "content": "The memory text, written as a statement about the user.",
    "source": "fact | preference | correction | pattern",
    "tags": ["tag1", "tag2"],
    "importance": 1.0
  }
]

Rules:
- importance: 1.5 for corrections (highest priority), 1.2 for preferences, 1.0 for facts/patterns
- tags: short lowercase strings relevant to the memory topic
- If nothing worth remembering happened, return an empty array: []
- Maximum 10 memories per session
- Each memory must be a complete, self-contained statement

Conversation to analyse:
"""


def summarize_session(
    session_id: str,
    messages: list[dict],
) -> int:
    """
    Extracts memories from a completed session and stores them in Supabase.

    Args:
        session_id: The session ID (used for logging only).
        messages:   The full list of message dicts from the session
                    [{"role": "user"|"assistant", "content": str}, ...]

    Returns:
        Number of memories stored. 0 if nothing was extracted or on failure.
    """
    if len(messages) < 2:
        log.debug(f"[{session_id}] Session too short to summarise — skipping.")
        return 0

    # Format conversation for the LLM
    convo_text = "\n".join(
        f"{m['role'].upper()}: {m['content']}"
        for m in messages
        if m["role"] in ("user", "assistant")
    )

    extraction_messages = [
        {
            "role": "user",
            "content": EXTRACTION_PROMPT + convo_text,
        }
    ]

    try:
        raw_res = chat(extraction_messages, max_tokens=800)
        raw_text = raw_res.get("content", "") if isinstance(raw_res, dict) else str(raw_res)
    except Exception as e:
        log.error(f"[{session_id}] Summariser LLM call failed: {e}")
        return 0

    # Parse the JSON response
    memories = _parse_extraction(raw_text, session_id)

    if not memories:
        return 0

    stored = store_memories_batch(memories)
    log.info(f"[{session_id}] Session summarised — {stored} memories stored.")
    return stored


def _parse_extraction(raw: str, session_id: str) -> list[dict]:
    """
    Parses the LLM's JSON output. Handles common formatting issues.
    Returns empty list on any parse failure — summarisation is non-critical.
    """
    if not raw or not raw.strip():
        return []

    text = raw.strip()

    # Strip markdown code fences if the LLM wrapped the JSON
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(
            line for line in lines
            if not line.strip().startswith("```")
        ).strip()

    try:
        data = json.loads(text)
        if not isinstance(data, list):
            log.warning(f"[{session_id}] Summariser returned non-list JSON — skipping.")
            return []

        valid = []
        for item in data:
            content = item.get("content", "").strip()
            source = item.get("source", "fact")
            if content and source in ("fact", "preference", "correction", "pattern"):
                valid.append({
                    "content": content,
                    "source": source,
                    "tags": item.get("tags", []),
                    "importance": float(item.get("importance", 1.0)),
                })

        return valid

    except json.JSONDecodeError as e:
        log.warning(f"[{session_id}] Failed to parse summariser output: {e}")
        log.debug(f"Raw output was: {raw[:300]}")
        return []
