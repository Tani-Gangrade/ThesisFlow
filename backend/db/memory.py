import pickle
from typing import Iterable

import numpy as np
from sqlalchemy.orm import Session

from db.models import Memory


def _to_blob(vector: Iterable[float]) -> bytes:
    return pickle.dumps(np.array(vector, dtype="float32"))


def _from_blob(blob: bytes) -> np.ndarray:
    return pickle.loads(blob)


def add_memory(db: Session, role: str, content: str, embedding: list[float] | None):
    memory = Memory(
        role=role,
        content=content,
        embedding=_to_blob(embedding) if embedding else None,
    )
    db.add(memory)
    db.commit()
    db.refresh(memory)
    return memory


def list_recent_memory(db: Session, limit: int = 20):
    return (
        db.query(Memory)
        .order_by(Memory.created_at.desc())
        .limit(limit)
        .all()
    )


def search_memory(db: Session, query_embedding: list[float], k: int = 5):
    memories = db.query(Memory).all()
    if not memories:
        return []

    query = np.array(query_embedding, dtype="float32")

    scored = []
    for m in memories:
        if not m.embedding:
            continue
        vec = _from_blob(m.embedding)
        denom = (np.linalg.norm(query) * np.linalg.norm(vec)) + 1e-10
        score = float(np.dot(query, vec) / denom)
        scored.append((score, m))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [m for _, m in scored[:k]]
