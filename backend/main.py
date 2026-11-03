"""
FastAPI application entry point.

Routes:
  GET  /health        — health check (for monitoring, Cloud Run probes)
  POST /chat          — single conversation turn
  POST /session/start — create a new session
  POST /session/end   — end a session and trigger summarisation
  GET  /download      — direct file download for mobile remote retrieval
"""

import logging
import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from agent.core import start_session, end_session, process_message
from routes.metrics import router as metrics_router
from routes.cli_bridge import router as cli_bridge_router
from tools.safety import is_safe_path

load_dotenv(override=True)


logging.basicConfig(
    level=logging.WARNING if os.getenv("ENVIRONMENT") == "production" else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger(__name__)

app = FastAPI(
    title="Luna",
    description="Personal autonomous AI assistant — backend API",
    version="0.1.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(metrics_router)
app.include_router(cli_bridge_router)


# ─────────────────────────────────────────────────────────────
# Request / response models
# ─────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    session_id: str
    text: str


class ChatResponse(BaseModel):
    session_id: str
    text: str
    type: str = "text"  # "text" | "image" | "code" | "download"
    images: list[dict] | None = None
    download_url: str | None = None
    file_name: str | None = None


class SessionResponse(BaseModel):
    session_id: str


# ─────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/download")
def download_file(filepath: str = Query(..., description="Path to local file")):
    """
    Direct File Download Endpoint — Allows mobile phone to download files from laptop.
    Enforces Path Traversal Protection (`is_safe_path`).
    """
    abs_path = os.path.abspath(filepath)
    if not os.path.exists(abs_path):
        raise HTTPException(status_code=404, detail=f"File not found: '{filepath}'")

    if not is_safe_path(abs_path):
        raise HTTPException(status_code=403, detail="Access denied: File outside safe workspace.")

    filename = os.path.basename(abs_path)
    return FileResponse(path=abs_path, filename=filename, media_type="application/octet-stream")


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
    except Exception as e:
        log.error(f"Chat turn error: {e}")
        res = {
            "text": "Sir, I encountered a temporary network glitch while processing your request. Please try again.",
            "type": "text"
        }

    return ChatResponse(
        session_id=body.session_id,
        text=res.get("text", ""),
        type=res.get("type", "text"),
        images=res.get("images"),
        download_url=res.get("download_url"),
        file_name=res.get("file_name"),
    )
