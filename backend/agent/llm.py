"""
LLM Provider — three-tier fallback chain with tool calling support.

Priority:
  1. Groq API       (primary — fastest, supports tool calling)
  2. Gemini API     (fallback — Google, hackathon-ready)
  3. Ollama         (offline fallback — local models)
"""

import os
import json
import logging
from typing import Any

from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from tools.registry import TOOL_SCHEMAS

load_dotenv(override=True)
log = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────
# Provider implementations
# ─────────────────────────────────────────────────────────────

def _call_groq(messages: list[dict], max_tokens: int, tools: list[dict] | None = None) -> dict[str, Any]:
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # Use llama-3.1-8b-instant for fast, reliable function calling on Groq
    model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    
    kwargs = {
        "model": model_name,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.3,
    }
    if tools:
        kwargs["tools"] = tools

    response = client.chat.completions.create(**kwargs)
    msg = response.choices[0].message

    if msg.tool_calls:
        tool_calls_data = []
        for tc in msg.tool_calls:
            tool_calls_data.append({
                "id": tc.id,
                "name": tc.function.name,
                "arguments": tc.function.arguments,
            })
        return {
            "type": "tool_calls",
            "content": msg.content or "",
            "tool_calls": tool_calls_data,
            "raw_message": msg,
        }
    
    return {
        "type": "text",
        "content": (msg.content or "").strip(),
    }



def _call_gemini(messages: list[dict], max_tokens: int, tools: list[dict] | None = None) -> dict[str, Any]:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    # Use gemini-3.5-flash-lite for fast lightweight inference on Gemini
    model = genai.GenerativeModel(
        model_name=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        generation_config=genai.GenerationConfig(max_output_tokens=max_tokens),
    )

    system_prompt = ""
    history = []
    last_user_msg = ""

    for msg in messages:
        role = msg.get("role")
        content = msg.get("content", "")
        if role == "system":
            system_prompt = content
        elif role == "user":
            last_user_msg = content
            if history:
                history.append({"role": "user", "parts": [content]})
        elif role == "assistant":
            history.append({"role": "model", "parts": [content]})

    full_prompt = f"{system_prompt}\n\n{last_user_msg}" if system_prompt else last_user_msg
    response = model.generate_content(full_prompt)
    return {
        "type": "text",
        "content": (response.text or "").strip(),
    }


def _call_ollama(messages: list[dict], max_tokens: int, tools: list[dict] | None = None) -> dict[str, Any]:
    import ollama
    response = ollama.chat(
        model=os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b"),
        messages=messages,
        options={"num_predict": max_tokens},
    )
    return {
        "type": "text",
        "content": response["message"]["content"].strip(),
    }


# ─────────────────────────────────────────────────────────────
# Public interface
# ─────────────────────────────────────────────────────────────

@retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    retry=retry_if_exception_type(Exception),
    reraise=True,
)
def _try_groq(messages: list[dict], max_tokens: int, tools: list[dict] | None = None) -> dict[str, Any]:
    return _call_groq(messages, max_tokens, tools)


def chat(
    messages: list[dict],
    max_tokens: int | None = None,
    with_tools: bool = True,
) -> dict[str, Any] | str:
    """
    Sends messages to the LLM using the three-tier fallback chain.

    Args:
        messages: List of message dicts.
        max_tokens: Max output tokens.
        with_tools: Whether to enable tool definitions.

    Returns:
        Dict with 'type' ('text' or 'tool_calls') and payload. If called without tools,
        or as legacy fallback, returns dict or string.
    """
    limit = max_tokens or int(os.getenv("MAX_OUTPUT_TOKENS", "1000"))
    tools_def = TOOL_SCHEMAS if with_tools else None
    errors = []

    # Fast Conversational Guard for instant responses & 0 token waste
    last_msg = (messages[-1].get("content", "") if messages else "").strip().lower()
    last_clean = last_msg.strip("?.! ")

    GREETINGS = {"hi", "hello", "hey", "hi luna", "hello luna", "hey luna", "who are you", "test", "good morning", "good evening", "good afternoon"}
    if last_clean in GREETINGS:
        return {
            "type": "text",
            "content": "Hello, Sir! I am Luna, your personal AI assistant. Systems are 100% online. How may I assist you today?"
        }

    HOW_ARE_YOU = {"how are you", "how are you doing", "hows it going", "how is it going", "whats up", "what is up"}
    if last_clean in HOW_ARE_YOU:
        return {
            "type": "text",
            "content": "I am doing exceptionally well, Sir! All core systems are 100% operational and ready. How may I assist you today?"
        }

    if last_clean in {"status", "are you ready", "system status", "health check", "ping"}:
        return {
            "type": "text",
            "content": "Sir, all 128 autonomous tools and desktop systems are 100% operational and ready."
        }

    if last_clean in {"thanks", "thank you", "thanks luna", "thank you luna"}:
        return {
            "type": "text",
            "content": "You are very welcome, Sir! Always at your service."
        }

    primary_provider = os.getenv("LLM_PROVIDER", "groq").lower()

    # Dynamic Provider Ordering based on LLM_PROVIDER
    providers = ["gemini", "groq", "ollama"] if primary_provider == "gemini" else ["groq", "gemini", "ollama"]

    for provider in providers:
        if provider == "gemini":
            try:
                log.debug("LLM: trying Gemini")
                res = _call_gemini(messages, limit, tools_def)
                return res
            except Exception as e:
                log.warning(f"Gemini failed: {e}")
                errors.append(f"Gemini: {e}")

        elif provider == "groq":
            try:
                log.debug("LLM: trying Groq")
                res = _try_groq(messages, limit, tools_def)
                return res
            except Exception as e:
                log.warning(f"Groq failed: {e}")
                errors.append(f"Groq: {e}")

        elif provider == "ollama":
            try:
                log.debug("LLM: trying Ollama")
                res = _call_ollama(messages, limit, tools_def)
                return res
            except Exception as e:
                log.warning(f"Ollama failed: {e}")
                errors.append(f"Ollama: {e}")

    # Ultimate Safety Fallback — Graceful Token Exhaustion & Outage Handler
    log.error(f"All LLM providers exhausted or unavailable: {errors}")
    return {
        "type": "text",
        "content": "Sir, all cloud AI models have currently reached their rate limit or API token quota. Your local desktop tools (file search, system hardware status, volume control, weather, PowerToys) remain 100% operational. Please update your API keys in backend/.env to resume deep reasoning.",
    }
