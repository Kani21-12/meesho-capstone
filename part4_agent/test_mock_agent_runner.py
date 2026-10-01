from pathlib import Path

from part4_agent.mock_agent_runner import run


FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_may_acceptance():
    result = run(
        "May",
        str(FIXTURES / "april.csv"),
        str(FIXTURES / "may.csv"),
    )

    assert result["validation_status"] == "valid"
    assert result["validation_errors"] == []

    assert [item["category"] for item in result["flagged_categories"]] == [
        "Ethnic Wear",
        "Western Wear",
        "Kids Wear",
    ]

    assert [item["mom_pct"] for item in result["flagged_categories"]] == [
        77.1,
        -23.6,
        -23.48,
    ]

    assert set(result["suppressed_categories"]) == {
        "Beauty & Personal Care",
        "Home & Kitchen",
    }

    assert result["escalated_categories"] == []
    assert result["action_taken"] == "drafted_and_held_for_approval"


def test_june_acceptance():
    result = run(
        "June",
        str(FIXTURES / "may.csv"),
        str(FIXTURES / "june.csv"),
    )

    assert result["validation_status"] == "valid"
    assert result["validation_errors"] == []

    assert [item["category"] for item in result["flagged_categories"]] == [
        "Ethnic Wear",
        "Home & Kitchen",
        "Kids Wear",
    ]

    assert [item["mom_pct"] for item in result["flagged_categories"]] == [
        -58.74,
        42.59,
        23.9,
    ]

    assert result["suppressed_categories"] == ["Western Wear"]

    categories = [
        item["category"]
        for item in result["flagged_categories"]
    ]

    assert "Beauty & Personal Care" not in categories
    assert "Beauty & Personal Care" not in result["suppressed_categories"]

    assert result["escalated_categories"] == []
    assert result["action_taken"] == "drafted_and_held_for_approval"


def test_corrupted_feed_hard_stop():
    result = run(
        "July",
        str(FIXTURES / "june.csv"),
        str(
            Path(__file__).resolve().parent.parent
            / "part2_engine"
            / "fixtures"
            / "corrupted_feed.csv"
        ),
    )

    assert result["validation_status"] == "invalid"

    assert result["validation_errors"] == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]

    assert result["flagged_categories"] == []
    assert result["suppressed_categories"] == []
    assert result["escalated_categories"] == []
    assert result["action_taken"] == "hard_stop"


def test_exact_boundary_is_escalated():
    result = run(
        "August",
        str(FIXTURES / "boundary_previous.csv"),
        str(FIXTURES / "boundary_current.csv"),
    )

    assert result["validation_status"] == "valid"
    assert result["flagged_categories"] == []
    assert result["suppressed_categories"] == []
    assert result["escalated_categories"] == ["Boundary Test"]
    assert result["action_taken"] == "drafted_and_held_for_approval"


def test_drafted_messages_contain_only_verified_mom_number():
    result = run(
        "May",
        str(FIXTURES / "april.csv"),
        str(FIXTURES / "may.csv"),
    )

    for item in result["flagged_categories"]:
        message = item["message"]

        assert item["category"] in message
        assert str(item["mom_pct"]) in message

        # The draft should not introduce the previous/current revenue
        # as extra numeric figures.
        assert str(item["previous_revenue"]) not in message
        assert str(item["current_revenue"]) not in message


def test_output_schema_has_exact_top_level_keys():
    result = run(
        "May",
        str(FIXTURES / "april.csv"),
        str(FIXTURES / "may.csv"),
    )

    assert set(result.keys()) == {
        "run_month",
        "validation_status",
        "validation_errors",
        "flagged_categories",
        "suppressed_categories",
        "escalated_categories",
        "action_taken",
    }