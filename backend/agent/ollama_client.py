import os
import json
from typing import Iterable

import httpx


def _base_url() -> str:
    return os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")


def required_models() -> dict[str, str]:
    return {
        "chat": os.getenv("OLLAMA_CHAT_MODEL", "phi3"),
        "embed": os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text"),
    }


def _model_matches(required: str, available: list[str]) -> bool:
    # Accept exact names and tag variants like `phi3:latest`.
    return any(name == required or name.split(":", 1)[0] == required for name in available)


def list_models() -> list[str]:
    base = _base_url()
    with httpx.Client(timeout=10.0) as client:
        resp = client.get(f"{base}/api/tags")
        resp.raise_for_status()
        data = resp.json()
    return [m.get("name", "") for m in data.get("models", [])]


def assert_ollama_ready():
    models = required_models()
    available = list_models()
    missing = [name for name in models.values() if not _model_matches(name, available)]
    if missing:
        raise RuntimeError(
            "Missing Ollama model(s): "
            + ", ".join(missing)
            + ". Install with: "
            + " ".join([f"`ollama pull {m}`" for m in missing])
        )


def embed_texts(texts: Iterable[str], model: str | None = None) -> list[list[float]]:
    model_name = model or os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    base = _base_url()

    embeddings: list[list[float]] = []
    with httpx.Client(timeout=60.0) as client:
        for text in texts:
            resp = client.post(
                f"{base}/api/embeddings",
                json={"model": model_name, "prompt": text},
            )
            resp.raise_for_status()
            data = resp.json()
            embeddings.append(data["embedding"])

    return embeddings


def chat_stream(
    messages: list[dict],
    model: str | None = None,
    temperature: float | None = None,
):
    model_name = model or os.getenv("OLLAMA_CHAT_MODEL", "phi3")
    base = _base_url()

    payload = {
        "model": model_name,
        "messages": messages,
        "stream": True,
    }
    if temperature is not None:
        payload["options"] = {"temperature": temperature}

    with httpx.Client(timeout=None) as client:
        with client.stream("POST", f"{base}/api/chat", json=payload) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line:
                    continue
                data = json.loads(line)
                if data.get("done"):
                    break
                message = data.get("message", {})
                content = message.get("content")
                if content:
                    yield content
