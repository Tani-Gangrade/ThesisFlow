def update_evidence(thesis_state, paper):
    for section in paper["mapped_sections"]:
        for claim in thesis_state["outline"]["Chapter 3"][section]["claims"]:
            claim["current_evidence"] += 1
