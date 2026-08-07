"""
LLM Provider — three-tier fallback chain.

Priority:
  1. Groq API       (primary — fastest, generous free tier)
  2. Gemini API     (fallback — Google, hackathon-ready)
  3. Ollama         (offline fallback — local models, zero cost)

Switching between providers requires no changes to callers.
All providers return a plain string response.
"""

import os
import logging
from typing import Generator

from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

load_dotenv()
log = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────
# Provider implementations
# ─────────────────────────────────────────────────────────────

def _call_groq(messages: list[dict], max_tokens: int) -> str:
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


def _call_gemini(messages: list[dict], max_tokens: int) -> str:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel(
        model_name=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        generation_config=genai.GenerationConfig(max_output_tokens=max_tokens),
    )

    # Convert OpenAI-style messages to Gemini format
    system_prompt = ""
    history = []
    last_user_msg = ""

    for msg in messages:
        role = msg["role"]
        content = msg["content"]
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
    return response.text.strip()


def _call_ollama(messages: list[dict], max_tokens: int) -> str:
    import ollama
    response = ollama.chat(
        model=os.getenv("OLLAMA_MODEL", "qwen2.5:4b"),
        messages=messages,
        options={"num_predict": max_tokens},
    )
    return response["message"]["content"].strip()


# ─────────────────────────────────────────────────────────────
# Public interface
# ─────────────────────────────────────────────────────────────

@retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    retry=retry_if_exception_type(Exception),
    reraise=True,
)
def _try_groq(messages: list[dict], max_tokens: int) -> str:
    return _call_groq(messages, max_tokens)


def chat(
    messages: list[dict],
    max_tokens: int | None = None,
) -> str:
    """
    Sends messages to the LLM using the three-tier fallback chain.

    Args:
        messages: List of {"role": "system"|"user"|"assistant", "content": str}
        max_tokens: Maximum output tokens. Defaults to env MAX_OUTPUT_TOKENS.

    Returns:
        Plain string response from whichever provider succeeded.

    Raises:
        RuntimeError: If all three providers fail.
    """
    limit = max_tokens or int(os.getenv("MAX_OUTPUT_TOKENS", "1000"))
    errors = []

    # Tier 1 — Groq
    try:
        log.debug("LLM: trying Groq")
        return _try_groq(messages, limit)
    except Exception as e:
        log.warning(f"Groq failed: {e}")
        errors.append(f"Groq: {e}")

    # Tier 2 — Gemini
    try:
        log.debug("LLM: falling back to Gemini")
        return _call_gemini(messages, limit)
    except Exception as e:
        log.warning(f"Gemini failed: {e}")
        errors.append(f"Gemini: {e}")

    # Tier 3 — Ollama (local)
    try:
        log.debug("LLM: falling back to local Ollama")
        return _call_ollama(messages, limit)
    except Exception as e:
        log.warning(f"Ollama failed: {e}")
        errors.append(f"Ollama: {e}")

    raise RuntimeError(
        "All LLM providers failed.\n" + "\n".join(errors)
    )
