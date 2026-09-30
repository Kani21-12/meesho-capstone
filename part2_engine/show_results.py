import csv
from pathlib import Path

from growth_engine import mom_growth, is_flagged, validate_feed


# --------------------------------------------------
# 1. Show corrupted feed validation results
# --------------------------------------------------

corrupted_file = Path(__file__).parent / "fixtures" / "corrupted_feed.csv"

valid, errors = validate_feed(str(corrupted_file))

print()
print("===== CORRUPTED FEED VALIDATION =====")
print(f"Valid: {valid}")
print("Errors:")

for error in errors:
    print(error)


# --------------------------------------------------
# 2. Read the clean Part 1 data
# --------------------------------------------------

clean_file = Path(__file__).parent / "fixtures" / "monthly_category_revenue.csv"

data = []

with open(clean_file, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        data.append(row)


# --------------------------------------------------
# 3. Create April, May and June revenue dictionaries
# --------------------------------------------------

april = {
    row["category"]: float(row["revenue"])
    for row in data
    if row["month"] == "April"
}

may = {
    row["category"]: float(row["revenue"])
    for row in data
    if row["month"] == "May"
}

june = {
    row["category"]: float(row["revenue"])
    for row in data
    if row["month"] == "June"
}


# --------------------------------------------------
# 4. Show May vs April
# --------------------------------------------------

print()
print("===== MAY VS APRIL =====")
print(f"{'Category':<27} {'MoM':>8}   {'Status'}")
print("-" * 52)

for category in april:
    growth = mom_growth(april[category], may[category])
    status = is_flagged(growth)

    print(f"{category:<27} {growth:>7.2f}%   {status}")


# --------------------------------------------------
# 5. Show June vs May
# --------------------------------------------------

print()
print("===== JUNE VS MAY =====")
print(f"{'Category':<27} {'MoM':>8}   {'Status'}")
print("-" * 52)

for category in may:
    growth = mom_growth(may[category], june[category])
    status = is_flagged(growth)

    print(f"{category:<27} {growth:>7.2f}%   {status}")


print()
print("===== PART 2 RESULTS DISPLAYED SUCCESSFULLY =====")