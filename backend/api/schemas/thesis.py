from pydantic import BaseModel

class ThesisCreate(BaseModel):
    title: str


class SectionCreate(BaseModel):
    thesis_id: int
    name: str


class ClaimCreate(BaseModel):
    section_id: int
    text: str
    required_evidence: int = 3
