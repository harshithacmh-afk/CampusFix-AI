def diagnose_cases(cases):
    if cases.empty:
        return {
            "likely_cause": "No similar historical cases found",
            "confidence": "Low",
            "evidence": []
        }

    cause_counts = cases["root_cause"].value_counts()

    likely_cause = cause_counts.index[0]
    count = cause_counts.iloc[0]

    confidence = f"{count}/{len(cases)} similar cases"

    evidence = cases[
        cases["root_cause"] == likely_cause
    ][
        ["case_id", "complaint", "root_cause", "resolution"]
    ].to_dict("records")

    return {
        "likely_cause": likely_cause,
        "confidence": confidence,
        "evidence": evidence
    }