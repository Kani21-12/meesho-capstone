import csv
from pathlib import Path


source_file = (
    Path(__file__).resolve().parent.parent
    / "part1_sql"
    / "output"
    / "monthly_category_revenue.csv"
)

output_folder = Path(__file__).resolve().parent / "fixtures"
output_folder.mkdir(exist_ok=True)


with open(source_file, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    rows = list(reader)


for month in ["April", "May", "June"]:

    output_file = output_folder / f"{month.lower()}.csv"

    month_rows = [
        row for row in rows
        if row["month"] == month
    ]

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "month",
                "category",
                "revenue",
                "n_orders",
            ],
        )

        writer.writeheader()
        writer.writerows(month_rows)

    print(f"Created: {output_file}")