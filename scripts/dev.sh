#!/usr/bin/env bash
set -euo pipefail

# Run the full local development stack:
# - Ollama must already be running on port 11434.
# - FastAPI starts on port 8000.
# - Streamlit starts on port 8501.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

OLLAMA_URL="${OLLAMA_BASE_URL:-http://127.0.0.1:11434}"
BACKEND_PORT="${BACKEND_PORT:-8000}"
STREAMLIT_PORT="${STREAMLIT_PORT:-8501}"

PYTHON_BIN="$ROOT_DIR/venv/bin/python"
STREAMLIT_BIN="$ROOT_DIR/venv/bin/streamlit"

BACKEND_PID=""
STREAMLIT_PID=""

fail() {
  echo "Error: $*" >&2
  exit 1
}

check_virtualenv() {
  [[ -x "$PYTHON_BIN" ]] || fail "Missing virtualenv. Run: make setup"
  [[ -x "$STREAMLIT_BIN" ]] || fail "Streamlit is not installed in venv. Run: source venv/bin/activate && pip install -r requirements.txt"
}

check_ollama() {
  if ! curl -sS "$OLLAMA_URL/api/tags" >/dev/null; then
    fail "Ollama is not running at $OLLAMA_URL. Start Ollama, then run: make dev"
  fi
}

check_port_free() {
  local port="$1"
  local service_name="$2"

  if lsof -i ":$port" >/dev/null 2>&1; then
    fail "Port $port is already in use by another process. Stop it, or set a different port for $service_name."
  fi
}

cleanup() {
  if [[ -z "$BACKEND_PID" && -z "$STREAMLIT_PID" ]]; then
    return
  fi

  echo
  echo "Shutting down ThesisFlow dev services..."

  if [[ -n "$BACKEND_PID" ]]; then
    kill "$BACKEND_PID" 2>/dev/null || true
  fi

  if [[ -n "$STREAMLIT_PID" ]]; then
    kill "$STREAMLIT_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

echo "Checking local development requirements..."
check_virtualenv
check_ollama
check_port_free "$BACKEND_PORT" "BACKEND_PORT"
check_port_free "$STREAMLIT_PORT" "STREAMLIT_PORT"

echo "Starting FastAPI backend: http://127.0.0.1:$BACKEND_PORT"
(
  cd "$ROOT_DIR/backend"
  "$PYTHON_BIN" -m uvicorn main:app --reload --port "$BACKEND_PORT"
) &
BACKEND_PID=$!

echo "Starting Streamlit app: http://127.0.0.1:$STREAMLIT_PORT"
(
  cd "$ROOT_DIR"
  "$STREAMLIT_BIN" run streamlit_app.py --server.port "$STREAMLIT_PORT"
) &
STREAMLIT_PID=$!

echo
echo "ThesisFlow is running."
echo "Backend:   http://127.0.0.1:$BACKEND_PORT"
echo "Frontend:  http://127.0.0.1:$STREAMLIT_PORT"
echo "Press Ctrl-C to stop both services."

# Bash 3 compatible process monitor.
# macOS still ships Bash 3, which does not support `wait -n`.
while true; do
  if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
    wait "$BACKEND_PID" || true
    fail "FastAPI backend stopped unexpectedly."
  fi

  if ! kill -0 "$STREAMLIT_PID" 2>/dev/null; then
    wait "$STREAMLIT_PID" || true
    fail "Streamlit app stopped unexpectedly."
  fi

  sleep 1
done
