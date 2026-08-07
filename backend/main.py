"""
FastAPI application entry point.

Routes:
  GET  /health        — health check (for monitoring, Cloud Run probes)
  POST /chat          — single conversation turn
  POST /session/start — create a new session
  POST /session/end   — end a session and trigger summarisation
"""

import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from agent.core import start_session, end_session, process_message
from routes.metrics import router as metrics_router

load_dotenv()


logging.basicConfig(
    level=logging.WARNING if os.getenv("ENVIRONMENT") == "production" else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(
    title="Luna",
    description="Personal autonomous AI assistant — backend API",
    version="0.1.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(metrics_router)



# ─────────────────────────────────────────────────────────────
# Request / response models
# ─────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    session_id: str
    text: str


class ChatResponse(BaseModel):
    session_id: str
    text: str
    type: str = "text"  # "text" | "image" | "code"
    images: list[dict] | None = None


class SessionResponse(BaseModel):
    session_id: str


# ─────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/session/start", response_model=SessionResponse)
def session_start():
    """Creates a new conversation session."""
    sid = start_session()
    return SessionResponse(session_id=sid)


@app.post("/session/end")
def session_end(body: SessionResponse):
    """Ends a session and triggers automatic memory summarisation."""
    end_session(body.session_id)
    return {"status": "ended", "session_id": body.session_id}


@app.post("/chat", response_model=ChatResponse)
def chat_turn(body: ChatRequest):
    """Processes one user message, executes any tool calls, and returns Luna's response."""
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="Text must not be empty.")

    try:
        res = process_message(body.session_id, body.text.strip())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    return ChatResponse(
        session_id=body.session_id,
        text=res.get("text", ""),
        type=res.get("type", "text"),
        images=res.get("images"),
    )

