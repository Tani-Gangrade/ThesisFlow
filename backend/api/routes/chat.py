from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from agent.ollama_client import chat_stream, embed_texts
from rag.store import search
from db.session import get_db
from db.memory import add_memory, search_memory

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    use_memory: bool = True
    use_rag: bool = True


@router.post("/chat-stream")
def chat_stream_route(req: ChatRequest, db: Session = Depends(get_db)):
    query = req.message.strip()
    if not query:
        return StreamingResponse(iter(["Message required."]), media_type="text/plain")

    query_embedding = embed_texts([query])[0]

    contexts = search(query_embedding) if req.use_rag else []
    memories = search_memory(db, query_embedding, k=5) if req.use_memory else []

    context_block = "\n".join([f"[DOC {i+1}] {c}" for i, c in enumerate(contexts)])
    memory_block = "\n".join(
        [f"[MEM {m.id}] ({m.role}) {m.content}" for m in memories]
    )

    system_prompt = (
        "You are MARA, a memory-augmented research assistant. "
        "Use memory when helpful. Use document context when available. "
        "If you use a document, cite it like [DOC 1]."
    )

    user_prompt = (
        f"Relevant memory:\n{memory_block or 'None'}\n\n"
        f"Relevant documents:\n{context_block or 'None'}\n\n"
        f"User message:\n{query}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    def token_generator():
        assistant_text = []
        for token in chat_stream(messages):
            assistant_text.append(token)
            yield token

        # Persist memory for both user and assistant
        add_memory(db, role="user", content=query, embedding=query_embedding)
        add_memory(
            db,
            role="assistant",
            content="".join(assistant_text),
            embedding=embed_texts(["".join(assistant_text)])[0] if assistant_text else None,
        )

    return StreamingResponse(token_generator(), media_type="text/plain")


# from fastapi import APIRouter, Depends # type: ignore
# from sqlalchemy.orm import Session # type: ignore

# from db.session import get_db
# from agent.llm import call_llm
# from agent.thesis_loader import load_thesis_state
# from agent.gaps import detect_gaps
# from agent.prompt import build_advisor_prompt

# router = APIRouter(prefix="/chat", tags=["Chat"])

# @router.post("")
# def chat(
#     message: dict,
#     db: Session = Depends(get_db)
# ):
#     user_message = message.get("message", "")

#     thesis_state = load_thesis_state(db)
#     gaps = detect_gaps(db)

#     prompt = build_advisor_prompt(
#         thesis_state=thesis_state,
#         gaps=gaps,
#         user_message=user_message
#     )

#     reply = call_llm(prompt)
#     return {"response": reply}
