from sqlalchemy.orm import Session # type: ignore
from db.models import Thesis

def load_thesis_state(db: Session) -> str:
    thesis = db.query(Thesis).first()
    if not thesis:
        return "No thesis defined."

    output = f"Thesis Title: {thesis.title}\n\n"

    for section in thesis.sections:
        output += f"Section: {section.name}\n"
        for claim in section.claims:
            output += (
                f"- Claim: {claim.text}\n"
                f"  Evidence: {claim.current_evidence}/{claim.required_evidence}\n"
            )
        output += "\n"

    return output
