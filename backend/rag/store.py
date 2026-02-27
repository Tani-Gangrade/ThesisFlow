import json
import os
import pickle

import hnswlib
import numpy as np

INDEX_FILE = "vector.index"
CHUNKS_FILE = "chunks.pkl"
META_FILE = "vector.meta.json"


def _load_index():
    if os.path.exists(INDEX_FILE) and os.path.exists(META_FILE):
        with open(META_FILE, "r", encoding="utf-8") as f:
            meta = json.load(f)
        dimension = meta.get("dimension")
        index = hnswlib.Index(space="cosine", dim=dimension)
        index.load_index(INDEX_FILE)
        chunks_store = pickle.load(open(CHUNKS_FILE, "rb"))
        return index, chunks_store, meta
    return None, [], {}


def _new_index(dimension: int, max_elements: int):
    index = hnswlib.Index(space="cosine", dim=dimension)
    index.init_index(max_elements=max_elements, ef_construction=200, M=16)
    index.set_ef(50)
    return index


def _normalize(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True) + 1e-10
    return vectors / norms


index, chunks_store, _meta = _load_index()


def store_embeddings(chunks, embeddings):
    global chunks_store
    global index

    vectors = np.array(embeddings, dtype="float32")
    vectors = _normalize(vectors)
    dimension = vectors.shape[1]

    if index is None or _meta.get("dimension") != dimension:
        index = _new_index(dimension, max_elements=max(1000, len(vectors)))
        chunks_store = []

    current = index.get_current_count()
    needed = current + len(vectors)
    if needed > index.get_max_elements():
        index.resize_index(max(needed, index.get_max_elements() * 2))

    ids = np.arange(len(chunks_store), len(chunks_store) + len(chunks))
    index.add_items(vectors, ids)
    chunks_store.extend(chunks)

    index.save_index(INDEX_FILE)
    pickle.dump(chunks_store, open(CHUNKS_FILE, "wb"))
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump({"dimension": dimension}, f)


def search(query_embedding, k=5):
    if index is None:
        return []
    vector = np.array([query_embedding], dtype="float32")
    vector = _normalize(vector)

    labels, _distances = index.knn_query(vector, k=k)

    return [chunks_store[i] for i in labels[0] if i < len(chunks_store)]
