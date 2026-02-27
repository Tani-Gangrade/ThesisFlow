# ThesisFlow Backend (Local-First MARA)

This backend runs fully locally and free:
- FastAPI API server
- Ollama for chat + embeddings
- HNSWLIB for document retrieval (RAG)
- SQLite for persistent memory

## Prereqs
1. Install Ollama: https://ollama.com
2. Pull models (one-time):
   - `ollama pull phi3`
   - `ollama pull nomic-embed-text`

## Setup
1. Create a Python virtualenv and install deps:
   - `python -m venv venv`
   - `source venv/bin/activate`
   - `pip install -r ../requirements.txt`

2. (Optional) Configure models:
   - `export OLLAMA_CHAT_MODEL=phi3`
   - `export OLLAMA_EMBED_MODEL=nomic-embed-text`
   - `export OLLAMA_BASE_URL=http://localhost:11434`

## Run
From `ThesisFlow/backend`:
- `uvicorn main:app --reload --port 8000`

## API
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
