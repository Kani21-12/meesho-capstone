from pathlib import Path
from masking import alias_for, assert_no_raw_names_leak


BASE = Path(__file__).parent

prompt_pack = (BASE / "prompt_pack.md").read_text(encoding="utf-8")
narrative = (BASE / "narrative_report.md").read_text(encoding="utf-8")


def check(name, condition):
    if condition:
        print(f"[PASS] {name}")
        return True
    else:
        print(f"[FAIL] {name}")
        return False


print("===== PART 3 ACCEPTANCE CHECK =====")

results = []


# 1. Prompt Pack sections
results.append(check(
    "Prompt Pack sections",
    all(section in prompt_pack for section in [
        "## Trigger",
        "## Input list",
        "## Prompt",
        "## Checklist"
    ])
))


# 2. Checklist has at least 4 concrete items
checklist_items = [
    "Number accuracy:",
    "Fact labeling:",
    "Hypothesis labeling:",
    "Actionability:",
    "Context completeness:",
    "No invented information:",
    "Audience fit:",
    "Privacy check:"
]

results.append(check(
    "Checklist >= 4 items",
    sum(item in prompt_pack for item in checklist_items) >= 4
))


# 3. May narrative exact percentage
results.append(check(
    "May Ethnic Wear +77.1%",
    "+77.1%" in narrative
))


# 4. June narrative exact percentage
results.append(check(
    "June Ethnic Wear -58.74%",
    "-58.74%" in narrative
))


# 5 and 6. Self-scoring section
# The self-scoring section comes after both worked narratives.
if "## Self-Scoring Against the 4 Refinement Criteria" in narrative:
    self_scoring = narrative.split(
        "## Self-Scoring Against the 4 Refinement Criteria",
        1
    )[1]
else:
    self_scoring = ""


may_scoring = self_scoring.split("### June", 1)[0]

results.append(check(
    "May self-scoring",
    all(item in may_scoring for item in [
        "Specificity:",
        "Audience fit:",
        "Completeness:",
        "Actionability:"
    ])
))


results.append(check(
    "June self-scoring",
    all(item in self_scoring for item in [
        "### June",
        "Specificity:",
        "Audience fit:",
        "Completeness:",
        "Actionability:"
    ])
))


# 7. Chart questions
results.append(check(
    "Chart questions 1-3",
    all(item in narrative for item in [
        "Which month had the highest total revenue?",
        "What percentage share does Ethnic Wear represent of April's total revenue?",
        "How do the four regions compare on total revenue?"
    ])
))


# 8. alias_for test
results.append(check(
    "alias_for(RS019)",
    alias_for("RS019") == "ALIAS-19"
))


# Raw reseller names from Part 1
raw_reseller_names = [
    "Mumbai Reseller 1",
    "Mumbai Reseller 4",
    "Hyderabad Reseller 6",
    "Lucknow Reseller 6",
    "Jaipur Reseller 5"
]


# 9. Final top-reseller narrative must be safe
if "## Top-Reseller Narrative" in narrative:
    top_reseller_narrative = narrative.split(
        "## Top-Reseller Narrative",
        1
    )[1]

    if "## Masking Test Expectations" in top_reseller_narrative:
        top_reseller_narrative = top_reseller_narrative.split(
            "## Masking Test Expectations",
            1
        )[0]
else:
    top_reseller_narrative = ""


results.append(check(
    "Final top-reseller narrative is safe",
    assert_no_raw_names_leak(
        top_reseller_narrative,
        raw_reseller_names
    )
))


# 10. Unsafe narrative must fail the masking check
unsafe_narrative = (
    "FACT: Mumbai Reseller 1 showed verified performance."
)

results.append(check(
    "Unsafe narrative",
    assert_no_raw_names_leak(
        unsafe_narrative,
        raw_reseller_names
    ) is False
))


# 11. Explicit negative-case test
results.append(check(
    "Negative-case test",
    "Mumbai Reseller 1" in unsafe_narrative
    and assert_no_raw_names_leak(
        unsafe_narrative,
        raw_reseller_names
    ) is False
))


print()

if all(results):
    print("PART 3 ACCEPTANCE: PASS")
else:
    print("PART 3 ACCEPTANCE: FAIL")