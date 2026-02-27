def build_advisor_prompt(
    thesis_state: str,
    gaps: list[str],
    user_message: str
) -> str:
    gap_text = "\n".join(gaps) if gaps else "No major gaps detected."

    return f"""
You are acting as a PhD thesis advisor.

CURRENT THESIS STATE:
{thesis_state}

EVIDENCE GAPS:
{gap_text}

USER MESSAGE:
{user_message}

TASK:
- Identify which thesis section this relates to
- Critically evaluate argument strength
- Point out weaknesses or missing evidence
- Suggest concrete next steps (papers to look for, sections to improve)

Be direct and constructive.
"""
