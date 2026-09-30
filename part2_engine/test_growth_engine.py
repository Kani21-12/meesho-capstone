from pathlib import Path

from growth_engine import mom_growth, is_flagged, validate_feed


def test_ethnic_wear_growth_is_flagged():
    # GIVEN
    previous = 104520.77
    current = 185107.61

    # WHEN
    growth = mom_growth(previous, current)
    result = is_flagged(growth)

    # THEN
    assert growth == 77.1
    assert result == "flagged"


def test_beauty_growth_is_not_flagged():
    # GIVEN
    previous = 35542.11
    current = 37559.07

    # WHEN
    growth = mom_growth(previous, current)
    result = is_flagged(growth)

    # THEN
    assert growth == 5.67
    assert result == "not_flagged"


def test_exact_boundary_is_escalated():
    # GIVEN
    previous = 100000
    current = 108000

    # WHEN
    growth = mom_growth(previous, current)
    result = is_flagged(growth)

    # THEN
    assert growth == 8.0
    assert result == "escalate_exact_boundary"


def test_corrupted_feed_is_rejected():
    # GIVEN
    fixture_path = Path(__file__).parent / "fixtures" / "corrupted_feed.csv"

    # WHEN
    valid, errors = validate_feed(str(fixture_path))

    # THEN
    assert valid is False

    assert errors == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]
def test_valid_monthly_category_revenue_feed():
    # GIVEN
    fixture_path = (
        Path(__file__).parent
        / "fixtures"
        / "monthly_category_revenue.csv"
    )

    # WHEN
    valid, errors = validate_feed(str(fixture_path))

    # THEN
    assert valid is True
    assert errors == []
        
def test_may_vs_april_full_mom_table():
    expected = {
        "Ethnic Wear": (77.1, "flagged"),
        "Western Wear": (-23.6, "flagged"),
        "Kids Wear": (-23.48, "flagged"),
        "Home & Kitchen": (-9.25, "flagged"),
        "Beauty & Personal Care": (-12.75, "flagged"),
    }

    # Read the Part 1 output
    import csv

    fixture_path = Path(__file__).parent / "fixtures" / "monthly_category_revenue.csv"

    data = []

    with open(fixture_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

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

    for category, (expected_growth, expected_status) in expected.items():
        growth = mom_growth(april[category], may[category])
        status = is_flagged(growth)

        assert growth == expected_growth
        assert status == expected_status


def test_june_vs_may_full_mom_table():
    expected = {
        "Ethnic Wear": (-58.74, "flagged"),
        "Western Wear": (11.97, "flagged"),
        "Kids Wear": (23.9, "flagged"),
        "Home & Kitchen": (42.59, "flagged"),
        "Beauty & Personal Care": (5.67, "not_flagged"),
    }

    # Read the Part 1 output
    import csv

    fixture_path = Path(__file__).parent / "fixtures" / "monthly_category_revenue.csv"

    data = []

    with open(fixture_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

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

    for category, (expected_growth, expected_status) in expected.items():
        growth = mom_growth(may[category], june[category])
        status = is_flagged(growth)

        assert growth == expected_growth
        assert status == expected_status    
