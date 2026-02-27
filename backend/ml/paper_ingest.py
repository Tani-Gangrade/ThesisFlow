def extract_paper_metadata(text: str) -> dict:
    prompt = f"""
    Extract:
    - Main contribution
    - Evidence type (benchmark, theory, deployment)
    - Limitations
    - Related thesis sections

    Paper:
    {text[:3000]}
    """
    # call LLM
