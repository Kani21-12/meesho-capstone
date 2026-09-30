# Reliable AI Narrative & Prompt-Pack Report

## 3.2 — Worked Narrative Report

### May — Ethnic Wear

**Context:**  
This update measures Ethnic Wear revenue for May compared with April.

**Insight — FACT:**  
Ethnic Wear revenue increased from INR 104520.77 in April to INR 185107.61 in May, representing **+77.1% month-on-month change**. This result is flagged because the absolute month-on-month movement exceeds the 8% threshold.

**Implication — HYPOTHESIS:**  
Confirm May's promotional calendar, campaign activity, and category-level stock availability for Ethnic Wear before treating the increase as a sustained demand trend. The data confirms the revenue movement, but it does not by itself prove the reason for the increase.

---

### June — Ethnic Wear

**Context:**  
This update measures Ethnic Wear revenue for June compared with May.

**Insight — FACT:**  
Ethnic Wear revenue decreased from INR 185107.61 in May to INR 76371.53 in June, representing **-58.74% month-on-month change**. This result is flagged because the absolute month-on-month movement exceeds the 8% threshold.

**Implication — HYPOTHESIS:**  
Check the May promotional calendar against June campaign activity, along with Ethnic Wear stock availability and any major assortment changes, before concluding that the June decline reflects a sustained fall in demand. The data confirms the decline but does not prove its cause.

---

## Self-Scoring Against the 4 Refinement Criteria

### May — Ethnic Wear

**Specificity:** Passes because the narrative names Ethnic Wear, April and May, and the exact verified revenue and +77.1% MoM result.

**Audience fit:** Passes because the narrative uses business language suitable for a regional manager rather than SQL or Python terminology.

**Completeness:** Passes because it contains context, a fact-based insight, and an actionable implication.

**Actionability:** Passes because it specifically asks the manager to check the promotional calendar, campaign activity, and stock availability.

### June — Ethnic Wear

**Specificity:** Passes because the narrative names Ethnic Wear, May and June, and the exact verified revenue and -58.74% MoM result.

**Audience fit:** Passes because the narrative focuses on business actions and avoids unnecessary technical implementation details.

**Completeness:** Passes because it contains context, a fact-based insight, and an actionable implication.

**Actionability:** Passes because it specifically asks the manager to compare campaign activity and check stock availability and assortment changes.

---

# 3.3 — Chart-Choice Justification

## Question 1 — Which month had the highest total revenue?

**Recommended chart: Bar chart.**

This is primarily a **univariate comparison** of one measure, total revenue, across three month categories. A vertical bar chart makes the relative heights immediately readable within 10 seconds and uses a zero-based y-axis so the visual difference is not exaggerated. The values are April = INR 419417.43, May = INR 444594.25, and June = INR 398055.24, so the chart makes the month-to-month comparison straightforward. A legend is unnecessary because there is only one series, and a 3D chart should be avoided because it can distort the comparison.

---

## Question 2 — What percentage share does Ethnic Wear represent of April's total revenue?

**Recommended chart: Pie chart.**

This is a **univariate part-to-whole** question: Ethnic Wear's April revenue is one component of April's total revenue. A pie chart can communicate the share within about 10 seconds when there are only a small number of meaningful parts, and the required result is **24.92%** (INR 104520.77 out of INR 419417.43). A legend should be used only if multiple slices require identification. A 3D pie chart should be avoided because perspective can distort perceived proportions. Unlike a bar chart, the zero-based y-axis rule does not apply to a pie chart because it has no y-axis.

---

## Question 3 — How do the four regions compare on total revenue?

**Recommended chart: Bar chart.**

This is a **univariate comparison** of one measure, total revenue, across four categorical regions. A bar chart with a zero-based y-axis allows North, West, South, and East to be compared quickly and accurately within 10 seconds. The verified regional totals are North = INR 337125.46, West = INR 333106.33, South = INR 316736.68, and East = INR 275098.45. Because there is only one revenue series, a legend is unnecessary. A 3D chart should be avoided because it can make differences between regions harder to judge accurately.

---

# 3.4 — Masking Policy

External-facing narratives must never expose a raw reseller name.

The five resellers from Part 1's HAVING query are represented only by their region and masked alias:

| Reseller ID | Region | External Alias |
|---|---|---|
| RS019 | West | ALIAS-19 |
| RS022 | West | ALIAS-22 |
| RS012 | South | ALIAS-12 |
| RS006 | North | ALIAS-06 |
| RS005 | North | ALIAS-05 |

The external narrative must use the region and alias only. Raw reseller names must not appear.

## Top-Reseller Narrative

**FACT:** The top-reseller result contains five resellers with verified total spend above INR 50000. The external-facing summary identifies them only by region and masked alias: West — ALIAS-19 and ALIAS-22; South — ALIAS-12; North — ALIAS-06 and ALIAS-05.

**HYPOTHESIS:** The regional manager should review the underlying category and monthly performance for these masked reseller accounts before deciding whether their current spend represents a sustained pattern or a temporary concentration.

No raw reseller name is included in this external-facing narrative.

---

## Masking Test Expectations

The masking implementation must satisfy:

```text
alias_for("RS019") == "ALIAS-19"