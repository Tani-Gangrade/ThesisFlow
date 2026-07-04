# ThesisFlow Backend (Memory Augmented Research Assistant)

This backend runs fully locally and free:
- FastAPI API server
- Ollama for chat + embeddings
- HNSWLIB for document retrieval (RAG)
- SQLite for persistent memory

## Local Development

ThesisFlow runs three local pieces:

- **Ollama** for local chat and embedding models
- **FastAPI** backend at `http://127.0.0.1:8000`
- **Streamlit** frontend at `http://127.0.0.1:8501`

### 1. Install Ollama models

Install Ollama from <https://ollama.com>, then pull the required models:

```bash
ollama pull phi3
ollama pull nomic-embed-text
```

Make sure Ollama is running before starting ThesisFlow. You can check it with:

```bash
curl http://127.0.0.1:11434/api/tags
```

### 2. Install Python dependencies

From the project root:

```bash
make setup
```

This creates `venv/` and installs everything from `requirements.txt`.

### 3. Start the app

```bash
make dev
```

This starts both services:

- FastAPI backend: `http://127.0.0.1:8000`
- Streamlit app: `http://127.0.0.1:8501`

Press `Ctrl-C` in the terminal to stop both.

### Useful Commands

```bash
make help      # Show available development commands
make setup     # Create venv and install dependencies
make dev       # Start backend and frontend together
make backend   # Start only FastAPI
make frontend  # Start only Streamlit
```

### Configuration

The dev script uses these defaults:

```bash
OLLAMA_BASE_URL=http://127.0.0.1:11434
BACKEND_PORT=8000
STREAMLIT_PORT=8501
```

You can override them when needed:

```bash
BACKEND_PORT=8010 STREAMLIT_PORT=8510 make dev
```

If startup fails, the most common causes are:

- Ollama is not running
- one of the required models has not been pulled
- port `8000` or `8501` is already in use
- dependencies were not installed into `venv/`

## Prerequisites
1. Install Ollama: https://ollama.com
2. Pull models (one-time):
   - `ollama pull phi3`
   - `ollama pull nomic-embed-text`

## Full Local App
From the project root:

```bash
make setup
make dev
```

This starts:

- FastAPI backend at `http://127.0.0.1:8000`
- Streamlit frontend at `http://127.0.0.1:8501`

## Backend Only
From the project root:

```bash
make backend
```

Or from `ThesisFlow/backend`:

```bash
../venv/bin/python -m uvicorn main:app --reload --port 8000
```

## Optional Model Configuration

```bash
export OLLAMA_CHAT_MODEL=phi3
export OLLAMA_EMBED_MODEL=nomic-embed-text
export OLLAMA_BASE_URL=http://localhost:11434
```

## API
### `GET /health`
Checks Ollama/model readiness, memory count, and RAG index stats.

### `POST /upload-pdf`
Uploads a PDF and indexes it into RAG.

### `POST /chat-stream`
Streams a response using memory + RAG.
Body:
```json
{
  "message": "What does the paper say about X?",
  "use_memory": true,
  "use_rag": true
}
```

### `GET /memory/recent?limit=20`
Returns recent persisted memories.

### `DELETE /memory`
Clears all persisted memory rows.

### `GET /rag/stats`
Returns vector/chunk counts and index metadata.
