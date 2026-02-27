from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.ingest import router as ingest_router
from api.routes.chat import router as chat_router
from db.database import init_db

app = FastAPI()

app.include_router(ingest_router)
app.include_router(chat_router)

@app.on_event("startup")
def startup():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "Backend running"}

