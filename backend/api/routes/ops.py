from fastapi import APIRouter, Depends
import httpx
from sqlalchemy.orm import Session

from agent.ollama_client import list_models, required_models
from agent.ollama_client import _model_matches
from db.memory import clear_memory, list_recent_memory, memory_count
from db.session import get_db
from rag.store import rag_stats

router = APIRouter()


@router.get("/health")
def health(db: Session = Depends(get_db)):
    required = required_models()
    try:
        available = list_models()
        missing = [m for m in required.values() if not _model_matches(m, available)]
        ollama_up = True
    except httpx.HTTPError:
        available = []
        missing = list(required.values())
        ollama_up = False
    return {
        "status": "ok" if not missing else "degraded",
        "ollama_up": ollama_up,
        "required_models": required,
        "available_models": available,
        "missing_models": missing,
        "memory_count": memory_count(db),
        "rag": rag_stats(),
    }


@router.get("/memory/recent")
def memory_recent(limit: int = 20, db: Session = Depends(get_db)):
    records = list_recent_memory(db, limit=limit)
    return {
        "count": len(records),
        "items": [
            {
                "id": r.id,
                "role": r.role,
                "content": r.content,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in records
        ],
    }


@router.delete("/memory")
def memory_clear(db: Session = Depends(get_db)):
    deleted = clear_memory(db)
    return {"status": "ok", "deleted": deleted}


@router.get("/rag/stats")
def rag_stats_route():
    return rag_stats()
