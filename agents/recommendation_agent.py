import pandas as pd


def recommend_fix(cases, likely_cause):

    matching_cases = cases[
        cases["root_cause"] == likely_cause
    ]

    if matching_cases.empty:

        return {
            "recommended_fix": "Inspect the equipment manually",
            "estimated_cost": "Unknown",
            "estimated_time": "Unknown",
            "urgency": "Medium"
        }

    # Get the most common recommended fix
    recommended_fix = (
        matching_cases["resolution"]
        .mode()
        .iloc[0]
    )

    # Convert cost values into numbers
    numeric_costs = (
        matching_cases["cost"]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    numeric_costs = pd.to_numeric(
        numeric_costs,
        errors="coerce"
    )

    # Calculate median only from valid numeric costs
    if numeric_costs.notna().any():

        estimated_cost = numeric_costs.median()

        estimated_cost = f"₹{estimated_cost:.0f}"

    else:

        estimated_cost = "Unknown"

    # Get the most common repair time
    estimated_time = (
        matching_cases["repair_time"]
        .mode()
        .iloc[0]
    )

    # Get the most common urgency
    urgency = (
        matching_cases["urgency"]
        .mode()
        .iloc[0]
    )

    return {
        "recommended_fix": recommended_fix,
        "estimated_cost": estimated_cost,
        "estimated_time": estimated_time,
        "urgency": urgency
    }