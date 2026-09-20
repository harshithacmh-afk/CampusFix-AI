def explain_diagnosis(
    complaint,
    cases,
    likely_cause,
    confidence,
    recommendation,
    urgency
):
    if cases.empty:
        return (
            "No sufficiently similar historical cases were found. "
            "A manual inspection is recommended."
        )

    evidence_count = len(
        cases[cases["root_cause"] == likely_cause]
    )

    explanation = (
        f"The complaint was compared with {len(cases)} historical maintenance cases. "
        f"{evidence_count} of the retrieved cases had the root cause "
        f"'{likely_cause}'. "
        f"Based on this historical evidence, the system identified "
        f"'{likely_cause}' as the likely cause with a confidence of "
        f"{confidence}. "
        f"The recommended action is '{recommendation['recommended_fix']}', "
        f"with an estimated cost of {recommendation['estimated_cost']} "
        f"and repair time of {recommendation['estimated_time']}. "
        f"The recommended urgency is {urgency}."
    )

    return explanation