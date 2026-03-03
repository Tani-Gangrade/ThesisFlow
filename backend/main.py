from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import logging
import time

from api.routes.ingest import router as ingest_router
from api.routes.chat import router as chat_router
from api.routes.ops import router as ops_router
from agent.ollama_client import assert_ollama_ready
from db.database import init_db

app = FastAPI()
logger = logging.getLogger("thesisflow")

app.include_router(ingest_router)
app.include_router(chat_router)
app.include_router(ops_router)

@app.on_event("startup")
def startup():
    init_db()
    try:
        assert_ollama_ready()
    except httpx.HTTPError as exc:
        raise RuntimeError(
            "Ollama is not reachable. Start Ollama at OLLAMA_BASE_URL before running backend."
        ) from exc

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_logger(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - started) * 1000
    logger.info(
        "%s %s -> %s (%.1fms)",
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response


@app.exception_handler(httpx.HTTPError)
async def httpx_exception_handler(_request: Request, exc: httpx.HTTPError):
    return JSONResponse(
        status_code=502,
        content={
            "error": "Upstream service request failed",
            "detail": str(exc),
        },
    )


@app.get("/")
def root():
    return {"status": "Backend running"}
