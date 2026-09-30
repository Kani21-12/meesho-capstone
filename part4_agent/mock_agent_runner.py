
import csv
import json
from pathlib import Path

from part2_engine.growth_engine import (
    validate_feed,
    mom_growth,
    is_flagged,
)


def load_revenue_csv(csv_path: str) -> tuple[str, dict[str, float]]:
    """
    Load a monthly category revenue CSV.

    Returns:
        month name
        dictionary of category -> revenue
    """
    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        return "", {}

    month = rows[0]["month"]

    revenue_by_category = {}

    for row in rows:
        revenue_by_category[row["category"]] = float(row["revenue"])

    return month, revenue_by_category


def fill_prompt_template(
    category: str,
    previous_revenue: float,
    current_revenue: float,
    mom_pct: float,
    month: str,
    prev_month: str,
) -> str:
    """
    Part 3 prompt-pack template-fill logic.

    Only verified supplied values are used for numerical claims.
    """

    return (
        f"Context: {category} revenue is being monitored from "
        f"{prev_month} to {month}.\n"
        f"FACT: {category} revenue changed by {mom_pct}% "
        f"from {prev_month} to {month}.\n"
        f"Implication: ACTION: Review the category performanceand "
        f"identify the appropriate business action based on the verified "
        f"revenue movement."
    )


def run(
    month: str,
    previous_month_csv: str,
    current_month_csv: str,
) -> dict:
    """
    Execute the Part 4 mock monitoring agent.

    The agent:
    - validates the current feed first
    - hard-stops on invalid data
    - calculates MoM growth for valid data
    - identifies flagged categories
    - escalates exact 8.0% boundary cases
    - drafts at most three flagged categories
    - suppresses additional flagged categories
    - returns one structured JSON-compatible dictionary
    """

    # ---------------------------------------------------------
    # 1. Load the monthly revenue feed and validate it
    # ---------------------------------------------------------

    validation_status, validation_errors = validate_feed(current_month_csv)

    if not validation_status:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": validation_errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "suppressed_mom_pct": {},
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }

    # ---------------------------------------------------------
    # 2. Feed is valid - load previous and current data
    # ---------------------------------------------------------

    previous_month, previous_revenue = load_revenue_csv(
        previous_month_csv
    )

    current_month, current_revenue = load_revenue_csv(
        current_month_csv
    )

    # Use the supplied run month as the official output month.
    # The CSV month is used for narrative context.
    run_month = month

    # ---------------------------------------------------------
    # 3 & 4. Calculate MoM and run is_flagged for every category
    # ---------------------------------------------------------

    flagged_candidates = []
    escalated_categories = []

    for category, current_value in current_revenue.items():

        if category not in previous_revenue:
            continue

        previous_value = previous_revenue[category]

        growth = mom_growth(
            previous_value,
            current_value,
        )

        status = is_flagged(growth)

        if status == "flagged":
            flagged_candidates.append(
                {
                    "category": category,
                    "mom_pct": growth,
                    "previous_revenue": previous_value,
                    "current_revenue": current_value,
                }
            )

        elif status == "escalate_exact_boundary":
            escalated_categories.append(category)

    # ---------------------------------------------------------
    # 5. Sort flagged categories by absolute MoM descending
    # ---------------------------------------------------------

    flagged_candidates.sort(
        key=lambda item: abs(item["mom_pct"]),
        reverse=True,
    )

    # ---------------------------------------------------------
    # 6. Draft at most the top 3 flagged categories
    # ---------------------------------------------------------

    top_three = flagged_candidates[:3]
    remaining_flagged = flagged_candidates[3:]

    flagged_categories = []

    for item in top_three:

        message = fill_prompt_template(
            category=item["category"],
            previous_revenue=item["previous_revenue"],
            current_revenue=item["current_revenue"],
            mom_pct=item["mom_pct"],
            month=current_month,
            prev_month=previous_month,
        )

        flagged_categories.append(
            {
                "category": item["category"],
                "mom_pct": item["mom_pct"],
                "previous_revenue": item["previous_revenue"],
                "current_revenue": item["current_revenue"],
                "drafted": True,
                "message": message,
            }
        )

    # ---------------------------------------------------------
    # 7. Suppress flagged categories beyond the top-3 cap
    # ---------------------------------------------------------

    suppressed_categories = [
        item["category"]
        for item in remaining_flagged
    ]

    # Keep the existing suppressed_categories contract as a list
    # of category names, while also exposing the verified MoM value
    # for acceptance checking and traceability.
    suppressed_mom_pct = {
        item["category"]: item["mom_pct"]
        for item in remaining_flagged
    }

    # ---------------------------------------------------------
    # 8. Emit structured result
    # ---------------------------------------------------------

    return {
        "run_month": run_month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged_categories,
        "suppressed_categories": suppressed_categories,
        "suppressed_mom_pct": suppressed_mom_pct,
        "escalated_categories": escalated_categories,
        "action_taken": "drafted_and_held_for_approval",
    }


if __name__ == "__main__":

    project_root = Path(__file__).resolve().parent.parent

    previous_csv = (
        project_root
        / "part1_sql"
        / "output"
        / "monthly_category_revenue.csv"
    )

    # This default demonstration uses the existing monthly feed.
    # Specific May/June scenarios are tested separately.
    result = run(
        month="May",
        previous_month_csv=str(previous_csv),
        current_month_csv=str(previous_csv),
    )

    print(json.dumps(result, indent=2))

