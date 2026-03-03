import os
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from rag.loader import extract_text_from_pdf
from rag.chunker import chunk_text
from rag.embedder import embed_chunks
from rag.store import store_embeddings

router = APIRouter()

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="Missing file name.")

        safe_name = Path(file.filename).name
        if not safe_name.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")

        os.makedirs("uploaded_papers", exist_ok=True)
        file_path = os.path.join("uploaded_papers", safe_name)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        text = extract_text_from_pdf(file_path)
        if not text.strip():
            raise HTTPException(status_code=400, detail="No extractable text found in PDF.")

        chunks = chunk_text(text)
        embeddings = embed_chunks(chunks)
        store_embeddings(chunks, embeddings)

        return {
            "status": "success",
            "chunks_stored": len(chunks)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}") from e
