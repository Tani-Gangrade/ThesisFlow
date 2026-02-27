from fastapi import UploadFile
from backend.agent.evidence_tracker import update_evidence
from backend.db import thesis_state
from backend.db.papers import save_paper
from backend.ml.paper_ingest import extract_paper_metadata


@router.post("/upload") # type: ignore
def upload_paper(file: UploadFile):
    text = extract_text(file) # type: ignore
    parsed = parse_paper_with_llm(text) # type: ignore
    save_paper(parsed)
    update_claim_evidence(parsed) # type: ignore
    return parsed
