def detect_gaps(thesis_state):
    gaps = []
    for chapter in thesis_state["outline"].values():
        for section in chapter.values():
            for claim in section["claims"]:
                if claim["current_evidence"] < claim["required_evidence"]:
                    gaps.append(claim)
    return gaps
