#!/usr/bin/env bash
# Luna Command Station — 1-Click Launch Script for macOS

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
mkdir -p "$DIR/logs"

echo "========================================================"
echo "         LUNA NEURAL COMMAND STATION (macOS)            "
echo "========================================================"

# 1. Start FastAPI Backend Kernel
echo "[1/2] Initializing Backend Kernel on http://localhost:8000..."
if [ -f "$DIR/backend/venv/bin/python" ]; then
    PY="$DIR/backend/venv/bin/python"
else
    PY="python3"
fi

cd "$DIR/backend"
"$PY" -m uvicorn main:app --host 0.0.0.0 --port 8000 > "$DIR/logs/backend.log" 2>&1 &
BACKEND_PID=$!
echo "      Backend running (PID: $BACKEND_PID)"

# 2. Start Next.js Cockpit Panel
echo "[2/2] Launching Cockpit Interface on http://localhost:3000..."
cd "$DIR/panel"
npm run dev > "$DIR/logs/panel.log" 2>&1 &
PANEL_PID=$!
echo "      Cockpit UI running (PID: $PANEL_PID)"

echo "========================================================"
echo "Luna online, Sir."
echo "Cockpit URL:  http://localhost:3000"
echo "Backend API:  http://localhost:8000"
echo "PIDs:         Backend=$BACKEND_PID, Panel=$PANEL_PID"
echo "To stop:      Run ./stop_luna.sh or kill PIDs"
echo "========================================================"

# Save PIDs for stop script
echo "$BACKEND_PID" > "$DIR/logs/backend.pid"
echo "$PANEL_PID" > "$DIR/logs/panel.pid"
