from backend.agent.gap_detector import detect_gaps


def thesis_agent(user_input, thesis_state, papers):
    relevant_papers = select_relevant_papers(user_input, papers) # type: ignore
    gaps = detect_gaps(thesis_state)

    prompt = f"""
    You are a PhD thesis advisor.

    Thesis:
    {thesis_state}

    Relevant papers:
    {relevant_papers}

    Evidence gaps:
    {gaps}

    User input:
    {user_input}

    Respond with:
    - Section relevance
    - Argument strength
    - Missing evidence
    - Next steps
    """

    return call_llm(prompt) # type: ignore
