# ThesisFlow Backend (Memory Augmented Research Assistant)

This backend runs fully locally and free:
- FastAPI API server
- Ollama for chat + embeddings
- HNSWLIB for document retrieval (RAG)
- SQLite for persistent memory

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
