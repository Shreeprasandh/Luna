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
        if "invalid" in session_id:
            raise ValueError(f"Session '{session_id}' not found. Call start_session() first.")
        _sessions[session_id] = []
        log.info(f"Auto-initialized session for ID: {session_id}")

    # Direct Local Intent Engine for Image/Photo Requests (Zero API Token Consumption)
    user_lower = user_text.lower().strip()
    if any(w in user_lower for w in ("pic", "photo", "picture", "image")) and any(w in user_lower for w in ("pull", "show", "get", "find", "search", "display", "look", "see", "him", "her", "of")):
        query_target = user_text
        working_mem = _sessions[session_id][-4:]
        context_text = " ".join([m.get("content", "") for m in working_mem])
        
        import re
        if any(ref in user_lower for ref in ("him", "her", "it", "them", "that", "this")) and context_text:
            names = re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+', context_text)
            if names:
                query_target = names[0]

        log.info(f"Direct Local Image Intent matched for target: {query_target}")
        from tools.registry import execute_tool
        res = execute_tool("image_search", {"query": query_target})
        if res.get("status") == "success":
            images = res.get("images", [])
            _sessions[session_id].append({"role": "user", "content": user_text})
            _sessions[session_id].append({"role": "assistant", "content": f"Here are the photos of {query_target}, Sir."})
            return {
                "text": f"Here are the photos of {query_target}, Sir.",
                "type": "image",
                "images": images
            }

    # Retrieve relevant memories from Supabase (only for queries > 3 words)
    memories: list[str] = []
    if len(user_text.strip().split()) > 3:
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

    # Action intent classifier — load tool schemas when explicit action or image query is requested
    ACTION_KEYWORDS = {
        "play", "search", "read", "write", "organize", "clean", "delete", "shred",
        "docker", "sql", "email", "calendar", "weather", "volume", "speedtest",
        "note", "todo", "git", "commit", "push", "schedule", "remind", "app",
        "launch", "open", "browser", "screenshot", "camera", "webcam", "health",
        "power", "battery", "process", "kill", "zip", "audit", "github", "wifi",
        "voice", "book", "quote", "news", "crop", "shield", "draft", "s3", "whois", "scan",
        "photo", "picture", "image", "show", "pull", "find", "display", "look", "view", "fetch", "get", "pic", "pics"
    }
    user_words = set(user_text.lower().split())
    use_tools = bool(user_words.intersection(ACTION_KEYWORDS))

    llm_res = chat(messages, with_tools=use_tools)

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

    current_turn = get_turn_count(session_id)
    log.info(f"[{session_id}] Turn {current_turn} complete")

    response_dict = {
        "text": final_text,
        "type": "image" if image_payload else "text",
    }
    if image_payload:
        response_dict["images"] = image_payload

    return response_dict
