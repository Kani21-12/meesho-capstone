import csv


def mom_growth(previous: float, current: float) -> float:
    return round((current - previous) / previous * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    if abs(mom_pct) > threshold:
        return "flagged"
    elif abs(mom_pct) < threshold:
        return "not_flagged"
    else:
        return "escalate_exact_boundary"


def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
    errors = []

    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for line_number, row in enumerate(reader, start=2):
            month = row["month"]
            category = row["category"]
            revenue = row["revenue"]

            if category == "":
                errors.append(
                    f"line {line_number}: missing category (month={month})"
                )

            if revenue == "":
                errors.append(
                    f"line {line_number}: missing revenue (category={category})"
                )
            else:
                try:
                    revenue_value = float(revenue)
                except ValueError:
                    errors.append(
                        f"line {line_number}: revenue not numeric: {revenue!r}"
                    )
                else:
                    if revenue_value < 0:
                        errors.append(
                            f"line {line_number}: negative revenue "
                            f"({revenue_value}) for category={category}"
                        )

    return (len(errors) == 0, errors)