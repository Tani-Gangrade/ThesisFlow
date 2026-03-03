#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! curl -sS "http://127.0.0.1:11434/api/tags" >/dev/null; then
  echo "Ollama is not running on http://127.0.0.1:11434"
  echo "Start Ollama first, then run: make dev"
  exit 1
fi

# Avoid duplicate Uvicorn process on port 8000.
if lsof -i :8000 >/dev/null 2>&1; then
  echo "Port 8000 is already in use. Stop the existing process and retry."
  exit 1
fi

# Avoid duplicate Streamlit process on port 8501.
if lsof -i :8501 >/dev/null 2>&1; then
  echo "Port 8501 is already in use. Stop the existing process and retry."
  exit 1
fi

cleanup() {
  if [[ -n "${BACKEND_PID:-}" ]]; then kill "$BACKEND_PID" 2>/dev/null || true; fi
  if [[ -n "${STREAMLIT_PID:-}" ]]; then kill "$STREAMLIT_PID" 2>/dev/null || true; fi
}
trap cleanup EXIT INT TERM

(
  cd "$ROOT_DIR/backend"
  source "$ROOT_DIR/venv/bin/activate"
  python -m uvicorn main:app --port 8000
) &
BACKEND_PID=$!

(
  cd "$ROOT_DIR"
  source "$ROOT_DIR/venv/bin/activate"
  streamlit run streamlit_app.py
) &
STREAMLIT_PID=$!

# Bash 3 compatible loop (macOS default bash does not support `wait -n`).
while true; do
  if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
    wait "$BACKEND_PID" || true
    exit 1
  fi

  if ! kill -0 "$STREAMLIT_PID" 2>/dev/null; then
    wait "$STREAMLIT_PID" || true
    exit 1
  fi

  sleep 1
done
