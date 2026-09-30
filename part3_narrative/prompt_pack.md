# Reusable Prompt Pack — Flagged Category Stakeholder Update

## Trigger

Run this prompt when a category's `is_flagged` result is `"flagged"`.

The prompt is intended for a flagged category whose verified revenue and month-on-month change have already been calculated by the SQL and Python pipeline.

---

## Input list

The prompt requires these verified placeholder variables:

- `{category}` — flagged category name
- `{previous_revenue}` — previous month's verified revenue
- `{current_revenue}` — current month's verified revenue
- `{mom_pct}` — verified month-on-month percentage change
- `{month}` — current month
- `{prev_month}` — previous month

Only these supplied values may be used for numerical claims.

---

## Prompt

You are preparing a concise stakeholder update for a regional manager.

Use the supplied verified values to write a Context → Insight → Implication narrative for the flagged category.

### Context
State what category is being measured and compare `{month}` with `{prev_month}`.

### Insight
State the verified month-on-month movement using `{mom_pct}`.

Every numerical value in the narrative must come directly from one of the supplied placeholders:
`{previous_revenue}`, `{current_revenue}`, or `{mom_pct}`.

Do not calculate, invent, estimate, round differently, or introduce any other number.

Label the numerical observation explicitly as **FACT**.

### Implication
Give one specific and actionable next step for the regional manager.

If a possible cause is suggested but is not directly proven by the supplied data, label it explicitly as **HYPOTHESIS**.

Do not present a hypothesis as a fact.

Write for a regional manager rather than a data engineer. Use clear business language and avoid unnecessary technical terminology.

Do not mention information that was not supplied in the input values.

---

## Checklist

Before the narrative is used, validate all of the following:

1. **Number accuracy:** Every number in the draft exactly matches a supplied placeholder value.

2. **Fact labeling:** The verified numerical insight is explicitly labeled **FACT**.

3. **Hypothesis labeling:** Any proposed cause that is not directly proven by the supplied data is explicitly labeled **HYPOTHESIS**.

4. **Actionability:** The recommendation names a specific business check or action rather than using a vague phrase such as "look into the category."

5. **Context completeness:** The narrative explicitly names both `{month}` and `{prev_month}` and identifies `{category}`.

6. **No invented information:** No additional revenue, percentage, order count, customer detail, cause, or other unsupported fact has been introduced.

7. **Audience fit:** The wording is understandable to a regional manager and does not require knowledge of SQL or Python.

8. **Privacy check:** If reseller information is included, only the approved reseller alias and region are used; raw reseller names are not exposed.