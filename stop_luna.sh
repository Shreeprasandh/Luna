#!/usr/bin/env bash
# Luna Command Station — Stop Script for macOS

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "Stopping Luna subsystems..."

if [ -f "$DIR/logs/backend.pid" ]; then
    PID=$(cat "$DIR/logs/backend.pid")
    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID"
        echo "Backend kernel stopped (PID: $PID)"
    fi
    rm -f "$DIR/logs/backend.pid"
fi

if [ -f "$DIR/logs/panel.pid" ]; then
    PID=$(cat "$DIR/logs/panel.pid")
    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID"
        echo "Cockpit panel stopped (PID: $PID)"
    fi
    rm -f "$DIR/logs/panel.pid"
fi

# Fallback cleanup for orphan processes
pkill -f "uvicorn main:app --host 0.0.0.0 --port 8000" 2>/dev/null || true
pkill -f "next dev" 2>/dev/null || true

echo "All Luna processes halted cleanly, Sir."
