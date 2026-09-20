def determine_urgency(cases, likely_cause):
    matching_cases = cases[
        cases["root_cause"] == likely_cause
    ]

    if matching_cases.empty:
        return "Medium"

    urgency_order = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Critical": 4
    }

    highest_urgency = max(
        matching_cases["urgency"],
        key=lambda value: urgency_order.get(value, 2)
    )

    return highest_urgency