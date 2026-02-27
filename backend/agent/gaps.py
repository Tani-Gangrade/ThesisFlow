from sqlalchemy.orm import Session # type: ignore
from db.models import Claim

def detect_gaps(db: Session):
    gaps = []
    claims = db.query(Claim).all()
    for c in claims:
        if c.current_evidence < c.required_evidence:
            gaps.append(
                f"{c.text} "
                f"(missing {c.required_evidence - c.current_evidence} evidence items)"
            )
    return gaps
