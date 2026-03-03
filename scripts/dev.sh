#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! curl -sS "http://127.0.0.1:11434/api/tags" >/dev/null; then
  echo "Ollama is not running on http://127.0.0.1:11434"
  echo "Start Ollama first, then run: make dev"
  exit 1
fi

# Avoid duplicate Next.js dev servers that cause lock-file failures.
if pgrep -f "next dev" >/dev/null 2>&1; then
  echo "An existing 'next dev' process is running. Stop it first (pkill -f 'next dev') and retry."
  exit 1
fi

# Avoid duplicate Uvicorn process on port 8000.
if lsof -i :8000 >/dev/null 2>&1; then
  echo "Port 8000 is already in use. Stop the existing process and retry."
  exit 1
fi

cleanup() {
  if [[ -n "${BACKEND_PID:-}" ]]; then kill "$BACKEND_PID" 2>/dev/null || true; fi
  if [[ -n "${FRONTEND_PID:-}" ]]; then kill "$FRONTEND_PID" 2>/dev/null || true; fi
}
trap cleanup EXIT INT TERM

(
  cd "$ROOT_DIR/backend"
  source "$ROOT_DIR/venv/bin/activate"
  python -m uvicorn main:app --port 8000
) &
BACKEND_PID=$!

(
  cd "$ROOT_DIR/frontend"
  npm run dev
) &
FRONTEND_PID=$!

# Bash 3 compatible loop (macOS default bash does not support `wait -n`).
while true; do
  if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
    wait "$BACKEND_PID" || true
    exit 1
  fi

  if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
    wait "$FRONTEND_PID" || true
    exit 1
  fi

  sleep 1
done
