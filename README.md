#📚 ThesisFlow
**ThesisFlow** is a local-first **Memory Augmented Research Assistant** for academic workflows.
It lets you upload research papers, index them with retrievel, and chat with a personal research assistant that remembers context across interactions. 

##❓ What It Does 
- Upload PDF papers and extract text
- Chunk and embed documents for retrieval
- Store long-term memory across chats
- Answer questions using both:
  - retrieved paper context
  - persistent memory
- Stream responses through a simple chat interface

##💻 Tech Stack
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


