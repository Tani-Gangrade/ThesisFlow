# 📚 ThesisFlow
**ThesisFlow** is a local-first **Memory Augmented Research Assistant** for academic workflows.
It lets you upload research papers, index them for retrieval, and chat with a personal research assistant that remembers context across interactions. 

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


## ❓ What It Does 
- Upload PDF papers and extract text
- Chunk and embed documents for retrieval
- Store long-term memory across chats
- Answer questions using both:
  - retrieved paper context
  - persistent memory
- Stream responses through a simple chat interface


## 💻 Tech Stack
- Streamlit for the chat interface
- FastAPI for the backend API
- Ollama for local model inference
- SQLite for persistent memory
- pdfplumber for PDF text extraction


## 🧩 Features
- No paid API required
- Persistent chat memory
- Retrieval-augmented generation (RAG)
- PDF ingestion pipeline
- Streaming responses


## 🎯 Current Limitations
- Designed primarily for local use
- Depends on locally running Ollama models
- Cloud deployment is possible, but not fully practical for free with the current architecture
- Uses local file-based storage for PDFs and vector index

-----
