from fastapi import APIRouter, UploadFile, File
from rag.loader import extract_text_from_pdf
from rag.chunker import chunk_text
from rag.embedder import embed_chunks
from rag.store import store_embeddings

router = APIRouter()

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_path = f"temp_{file.filename}"

        with open(file_path, "wb") as f:
            f.write(await file.read())

        text = extract_text_from_pdf(file_path)
        chunks = chunk_text(text)
        embeddings = embed_chunks(chunks)
        store_embeddings(chunks, embeddings)

        return {
            "status": "success",
            "chunks_stored": len(chunks)
        }

    except Exception as e:
        print("UPLOAD ERROR:", e)
        return {"error": str(e)}

