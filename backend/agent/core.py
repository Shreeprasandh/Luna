"""
Luna Agent Core — the brain of each conversation.

Handles:
- Session lifecycle (start, turn, end)
- Memory retrieval before each LLM call
- Context assembly
- LLM invocation via the fallback chain
- Post-session summarisation (writes new memories)
"""

import os
import uuid
import logging
from datetime import datetime

from dotenv import load_dotenv

from agent.persona import build_system_prompt
from agent.llm import chat
from agent.summarizer import summarize_session

load_dotenv()
log = logging.getLogger(__name__)

# In-memory session store: session_id -> list of message dicts
_sessions: dict[str, list[dict]] = {}

MAX_TURNS = int(os.getenv("SESSION_MAX_TURNS", "10"))
MAX_WORKING_MEMORY_TURNS = 6  # last N turns kept in context


# ─────────────────────────────────────────────────────────────
# Session management
# ─────────────────────────────────────────────────────────────

def start_session() -> str:
    """Creates a new session and returns its ID."""
    session_id = str(uuid.uuid4())
    _sessions[session_id] = []
    log.info(f"Session started: {session_id}")
    return session_id


def end_session(session_id: str) -> None:
    """
    Ends the session, runs the summarizer to extract memories,
    then cleans up working memory.
    """
    messages = _sessions.get(session_id, [])

    if messages:
        # Run summarizer in a fire-and-forget manner
        # Failures here are logged but never surface to the user
        try:
            summarize_session(session_id, messages)
        except Exception as e:
            log.error(f"Summarizer failed for session {session_id}: {e}")

    if session_id in _sessions:
        del _sessions[session_id]

    log.info(f"Session ended: {session_id}")


def get_turn_count(session_id: str) -> int:
    """Returns the number of completed turns in the session."""
    turns = _sessions.get(session_id, [])
    return len([m for m in turns if m["role"] == "user"])


# ─────────────────────────────────────────────────────────────
# Core conversation turn
# ─────────────────────────────────────────────────────────────

def process_message(session_id: str, user_text: str) -> str:
    """
    Processes one user message and returns Luna's response.

    Args:
        session_id: Active session ID from start_session().
        user_text: The user's raw input text.

    Returns:
        Luna's response as a plain string.

    Raises:
        ValueError: If the session does not exist.
        RuntimeError: If all LLM providers fail.
    """
    if session_id not in _sessions:
        raise ValueError(f"Session '{session_id}' not found. Call start_session() first.")

    turn_count = get_turn_count(session_id)
    if turn_count >= MAX_TURNS:
        return (
            "Sir, we have reached the session limit. "
            "Say 'goodbye' to end this session and start fresh."
        )

    # Retrieve relevant memories from Supabase (best-effort — non-blocking)
    memories: list[str] = []
    try:
        from agent.memory import retrieve_relevant_memories
        memories = retrieve_relevant_memories(user_text)
    except Exception as e:
        log.warning(f"Memory retrieval skipped: {e}")

    # Build system prompt with injected memories
    system_prompt = build_system_prompt(memories=memories if memories else None)

    # Assemble messages: system + recent working memory + new user message
    working_memory = _sessions[session_id][-MAX_WORKING_MEMORY_TURNS * 2:]
    messages = (
        [{"role": "system", "content": system_prompt}]
        + working_memory
        + [{"role": "user", "content": user_text}]
    )

    # Call LLM via fallback chain
    response = chat(messages)

    # Update working memory
    _sessions[session_id].append({"role": "user", "content": user_text})
    _sessions[session_id].append({"role": "assistant", "content": response})

    log.info(f"[{session_id}] Turn {turn_count + 1} complete")
    return response
