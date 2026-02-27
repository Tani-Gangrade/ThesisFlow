from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from db.models import Thesis, Section, Claim
from api.schemas.thesis import (
    ThesisCreate, SectionCreate, ClaimCreate
)

router = APIRouter(prefix="/thesis", tags=["Thesis"])

@router.post("/create")
def create_thesis(
    payload: ThesisCreate,
    db: Session = Depends(get_db)
):
    thesis = Thesis(title=payload.title)
    db.add(thesis)
    db.commit()
    db.refresh(thesis)
    return thesis

@router.post("/section")
def add_section(
    payload: SectionCreate,
    db: Session = Depends(get_db)
):
    section = Section(
        thesis_id=payload.thesis_id,
        name=payload.name
    )
    db.add(section)
    db.commit()
    db.refresh(section)
    return section

@router.post("/claim")
def add_claim(
    payload: ClaimCreate,
    db: Session = Depends(get_db)
):
    claim = Claim(
        section_id=payload.section_id,
        text=payload.text,
        required_evidence=payload.required_evidence,
        current_evidence=0
    )
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return claim
