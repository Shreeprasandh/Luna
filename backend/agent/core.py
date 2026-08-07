"""
Luna Agent Core — session management and tool-execution loop.
"""

import os
import uuid
import json
import logging
from typing import Any
from datetime import datetime

from dotenv import load_dotenv

from agent.persona import build_system_prompt
from agent.llm import chat
from tools.registry import execute_tool

load_dotenv()
log = logging.getLogger(__name__)

# In-memory session store: session_id -> list of message dicts
_sessions: dict[str, list[dict]] = {}

MAX_TURNS = int(os.getenv("SESSION_MAX_TURNS", "10"))
MAX_WORKING_MEMORY_TURNS = 6
MAX_TOOL_CALLS_PER_TURN = int(os.getenv("MAX_TOOL_CALLS_PER_TURN", "3"))


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
    from agent.summarizer import summarize_session

    messages = _sessions.get(session_id, [])

    if messages:
        try:
            summarize_session(session_id, messages)
        except Exception as e:
            log.error(f"Summarizer failed for session {session_id}: {e}")

    if session_id in _sessions:
        del _sessions[session_id]

    log.info(f"Session ended: {session_id}")


def get_turn_count(session_id: str) -> int:
    """Returns the number of completed user turns in the session."""
    turns = _sessions.get(session_id, [])
    return len([m for m in turns if m.get("role") == "user"])


# ─────────────────────────────────────────────────────────────
# Core conversation turn with tool execution loop
# ─────────────────────────────────────────────────────────────

def process_message(session_id: str, user_text: str) -> dict[str, Any]:
    """
    Processes one user message, executes tool calls if needed, and returns Luna's response.

    Args:
        session_id: Active session ID.
        user_text: Raw user text.

    Returns:
        Dict with 'text', 'type' ('text'|'image'|'code'), and optional payload (e.g. 'images').
    """
    if session_id not in _sessions:
        raise ValueError(f"Session '{session_id}' not found. Call start_session() first.")

    # Check for goodbye or exit intent to end session safely
    if any(w in user_text.lower() for w in ("goodbye", "exit session", "end session")):
        end_session(session_id)
        return {
            "text": "Session summarized and ended, Sir. Have a fantastic day!",
            "type": "text",
        }

    turn_count = get_turn_count(session_id)
    if turn_count >= MAX_TURNS:
        end_session(session_id)
        return {
            "text": "Sir, we reached the turn limit for this session. I have summarized our context to memory and started a fresh session for you.",
            "type": "text",
        }

    # Retrieve relevant memories from Supabase
    memories: list[str] = []
    try:
        from agent.memory import retrieve_relevant_memories
        memories = retrieve_relevant_memories(user_text)
    except Exception as e:
        log.warning(f"Memory retrieval skipped: {e}")

    system_prompt = build_system_prompt(memories=memories if memories else None)
    working_memory = _sessions[session_id][-MAX_WORKING_MEMORY_TURNS * 2:]

    messages = (
        [{"role": "system", "content": system_prompt}]
        + working_memory
        + [{"role": "user", "content": user_text}]
    )

    # Call LLM with tools enabled
    llm_res = chat(messages, with_tools=True)

    tool_results_summary = []
    image_payload = []

    # Check if tool execution was requested
    if isinstance(llm_res, dict) and llm_res.get("type") == "tool_calls":
        tool_calls = llm_res.get("tool_calls", [])[:MAX_TOOL_CALLS_PER_TURN]
        log.info(f"[{session_id}] Executing {len(tool_calls)} tool calls")

        # Append assistant's tool call message
        messages.append({
            "role": "assistant",
            "content": llm_res.get("content", ""),
            "tool_calls": [
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": {"name": tc["name"], "arguments": tc["arguments"]}
                } for tc in tool_calls
            ]
        })

        for tc in tool_calls:
            t_name = tc["name"]
            t_args = tc["arguments"]
            res = execute_tool(t_name, t_args)

            if t_name == "image_search" and res.get("status") == "success":
                image_payload = res.get("images", [])

            tool_results_summary.append(f"Tool '{t_name}' returned: {json.dumps(res)}")

            # Add tool result message
            messages.append({
                "role": "tool",
                "tool_call_id": tc["id"],
                "content": json.dumps(res),
            })

        # Second LLM call: summarize tool output for the user
        final_res = chat(messages, with_tools=False)
        final_text = final_res.get("content", "") if isinstance(final_res, dict) else str(final_res)

    else:
        final_text = llm_res.get("content", "") if isinstance(llm_res, dict) else str(llm_res)

    # Save to session working memory
    _sessions[session_id].append({"role": "user", "content": user_text})
    _sessions[session_id].append({"role": "assistant", "content": final_text})

    log.info(f"[{session_id}] Turn {turn_count + 1} complete")

    response_dict = {
        "text": final_text,
        "type": "image" if image_payload else "text",
    }
    if image_payload:
        response_dict["images"] = image_payload

    return response_dict
