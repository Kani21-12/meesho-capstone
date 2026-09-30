# Meesho Reseller Growth & Alert Intelligence Pipeline

## Project Overview

This project implements a reliable, repeatable Analytics and AI workflow for monitoring reseller-category revenue and generating controlled growth alerts.

The complete workflow is:

**SQL → Python Guardrails → Reliable Narrative → Agentic Workflow → Human Approval**

The project uses a fixed-seeded dataset so that the calculations and downstream results are reproducible and can be verified against the required acceptance criteria.

The complete pipeline is designed to run locally with **zero API keys, paid services, or hosted accounts**.

---

## Requirements

* Python 3.x
* SQLite
* `pytest` for running the test suites
* No external API keys
* No paid or account-gated services

Install the Python test dependency if needed:

```powershell
python -m pip install pytest
```

The complete project runs locally/offline. The AI narrative functionality uses deterministic template-based logic and does not require a real LLM API.

---

# Dataset Generation

The input dataset can be regenerated using the provided deterministic dataset generator.

From the project root:

```powershell
python data\generate_dataset.py
```

This generates:

```text
data/resellers.csv
data/orders.csv
data/meesho_reseller.db
```

The generator uses a fixed seed so that the dataset and downstream calculations are reproducible.

After regenerating the dataset, run the Parts in order.

---

# Running the Pipeline

The project is organized as four connected Parts:

```text
Part 1 → Part 2 → Part 3 → Part 4
```

The Parts are not independent implementations of the same calculation. Each stage uses verified information or rules established by the earlier stages.

---

# Part 1 — SQL Analytics

## Purpose

Part 1 computes the core business numbers using SQL against the generated SQLite database.

The SQL analysis produces:

* Monthly revenue by category
* Region-wise revenue and order counts
* Top resellers
* Zero-order resellers
* June delivered AOV

The SQL queries are stored in:

```text
part1_sql/queries.sql
```

## Run

From the project root:

```powershell
python part1_sql\run_queries.py
```

The generated outputs are written to:

```text
part1_sql/output/
```

Important output files include:

```text
monthly_category_revenue.csv
region_revenue_orders.csv
top_resellers.csv
zero_order_resellers.csv
zero_order_count_test.csv
june_delivered_aov.csv
```

The main downstream input for Part 2 is:

```text
part1_sql/output/monthly_category_revenue.csv
```

This file contains the monthly category revenue values used by the growth-detection engine.

## Workflow connection

**Part 1 → Part 2** follows the workflow pattern:

> **Compute the real business numbers via SQL first, then hand the verified numbers to the next stage.**

This separates authoritative business calculations from the Python guardrail and decision logic.

---

# Part 2 — Python Guardrail & Growth-Detection Engine

## Purpose

Part 2 takes the monthly category revenue data produced by Part 1 and applies Python validation and growth-detection logic.

The engine:

* Validates the incoming data feed
* Detects invalid data such as negative revenue and missing required fields
* Calculates month-over-month growth
* Applies the configured growth threshold
* Flags categories requiring attention
* Produces structured results for downstream narrative and agent processing

The main implementation is:

```text
part2_engine/growth_engine.py
```

Test fixtures are stored in:

```text
part2_engine/fixtures/
```

## Run tests

From the project root:

```powershell
pytest -q part2_engine\test_growth_engine.py
```

To display the validation and growth results:

```powershell
python part2_engine\show_results.py
```

## Workflow connection

**Part 2 → Part 3** follows the pattern:

> **Validate and compute first, then allow the narrative layer to use only verified results.**

Part 2 therefore acts as a guardrail between the SQL analytics layer and the narrative layer.

Part 2's verified growth and flag results are also used by **Part 4's agent runner**.

---

# Part 3 — Reliable AI Narrative & Prompt Pack

## Purpose

Part 3 defines the controlled narrative-generation approach for verified growth signals.

It contains:

```text
part3_narrative/prompt_pack.md
part3_narrative/narrative_report.md
part3_narrative/masking.py
part3_narrative/verify_part3.py
```

The prompt pack defines:

* Trigger conditions
* Required inputs
* Prompt structure
* Narrative requirements
* Validation/checklist rules
* Privacy and masking requirements

The narrative report demonstrates the resulting business narratives using verified values.

The masking module prevents internal reseller identifiers from being exposed in the narrative.

The narrative process is deterministic and offline. It does not require an external LLM API or API key.

## Run acceptance verification

From the project root:

```powershell
python part3_narrative\verify_part3.py
```

## Workflow connection

**Part 2 → Part 3** follows:

> **Verified analytical signal → controlled narrative template → validation**

Part 3 uses the verified results from Part 2 rather than independently calculating business values.

**Part 3 → Part 4** provides the controlled narrative structure that the agent workflow can use when preparing report drafts.

---

# Part 4 — Agentic Workflow

## Purpose

Part 4 demonstrates an agent-style reporting workflow using the verified analytical logic from Part 2 and the controlled narrative/reporting structure from Part 3.

The Part 4 workflow follows:

> **Intake → Summary → Report Draft → Validate → Human Approval**

The agent runner is:

```text
part4_agent/mock_agent_runner.py
```

The agent specification is:

```text
part4_agent/agent_spec.md
```

Additional Part 4 files include:

```text
part4_agent/create_fixtures.py
part4_agent/test_mock_agent_runner.py
part4_agent/fixtures/
```

## Run

From the project root:

```powershell
python -m part4_agent.mock_agent_runner
```

Run the Part 4 tests with:

```powershell
python -m pytest part4_agent/test_mock_agent_runner.py -v
```

## Part 4 behavior

The Part 4 runner reuses the Part 2 functions for validation and month-over-month growth detection.

It:

1. Validates the incoming feed.
2. Hard-stops when the feed is invalid.
3. Calculates and evaluates month-over-month growth.
4. Selects flagged categories for drafting.
5. Limits drafted notifications to the required maximum.
6. Records suppressed flagged categories.
7. Handles exact-threshold escalation cases separately.
8. Produces structured report/notification results.
9. Holds drafted notifications for human approval.
10. Does not automatically send notifications.

The runner imports the Part 2 engine functions rather than duplicating their implementation.

## Workflow connection

**Part 2 → Part 4** follows:

> **Verified data → guardrails → flagged signals → controlled agent workflow**

**Part 3 → Part 4** provides the controlled narrative/reporting structure used by the workflow.

Part 4 therefore orchestrates the earlier components rather than replacing the verified analytical calculations.

---

# How the Parts Connect

The complete pipeline is:

```text
Dataset Generator
       ↓
Part 1 — SQL Analytics
       ↓
monthly_category_revenue.csv
       ↓
Part 2 — Python Guardrail & Growth Engine
       ↓
Validated data + MoM growth + flagged categories
       ↓
   ┌───────────────────────┐
   ↓                       ↓
Part 3                  Part 4
Narrative               Agent Runner
Templates               + Part 2 Guardrails
   ↓                       ↓
Controlled              Intake → Summary
Narrative               → Report Draft
                           → Validate
   └───────────┬───────────┘
               ↓
        Human Approval
```

More specifically:

* **Part 1's SQL output feeds Part 2's growth engine.**
* **Part 2's validated growth results feed Part 3's narrative templates.**
* **Part 2's verified growth and flag results are also used by Part 4's agent runner.**
* **Part 3 provides the controlled narrative/reporting structure used by Part 4.**
* **Part 4 combines the verified analytical logic and controlled narrative workflow into an agentic reporting process.**
* **Nothing is automatically sent; final approval remains with a human.**

This design follows the principle of computing and validating business numbers programmatically before using them in an AI-style narrative or agent workflow.

---

# Workflow Pattern Mapping

| Part   | Implementation                            | Workflow pattern                                            |
| ------ | ----------------------------------------- | ----------------------------------------------------------- |
| Part 1 | SQL analytics                             | Compute verified business numbers first                     |
| Part 2 | Python guardrails and growth detection    | Validate → Compute → Flag                                   |
| Part 3 | Prompt pack, masking and narrative report | Verified Inputs → Controlled Narrative → Validate           |
| Part 4 | Mock agent runner                         | Intake → Summary → Report Draft → Validate → Human Approval |

The overall workflow is:

> **Compute → Validate → Narrate → Orchestrate → Approve**

Part 1 → Part 2 specifically demonstrates:

> **Compute real numbers via SQL first, then hand off verified data.**

Part 4 demonstrates:

> **Intake → Summary → Report Draft → Validate → Human Approval.**

---

# Zero API Keys and Offline Execution

The complete project runs with **zero API keys configured**.

No OpenAI, Gemini, Anthropic, or other external AI API is required.

No paid subscription or hosted account is required.

The AI narrative portion is implemented as deterministic, offline template-based processing. The project does not depend on a live LLM call for any acceptance criterion.

The complete workflow can therefore be executed locally using:

* The generated CSV data
* SQLite
* SQL queries
* Python logic
* Prompt templates
* Validation functions
* The mock agent runner
* Automated tests

This ensures that the complete pipeline remains reproducible and testable without external services.

---

# Recommended Run Order

From the project root, run the following in order.

## 1. Regenerate the dataset

```powershell
python data\generate_dataset.py
```

## 2. Run Part 1

```powershell
python part1_sql\run_queries.py
```

## 3. Run Part 2 tests

```powershell
pytest -q part2_engine\test_growth_engine.py
```

Optionally display the Part 2 results:

```powershell
python part2_engine\show_results.py
```

## 4. Run Part 3 acceptance verification

```powershell
python part3_narrative\verify_part3.py
```

## 5. Run Part 4

```powershell
python -m part4_agent.mock_agent_runner
```

Then run the Part 4 tests:

```powershell
python -m pytest part4_agent/test_mock_agent_runner.py -v
```

---

# Reproducibility

The dataset generator uses a fixed seed, allowing the input dataset to be regenerated consistently.

The pipeline then processes the data in a controlled sequence:

```text
Generated Dataset
      ↓
SQL Calculations
      ↓
Python Validation & Growth Detection
      ↓
Reliable Narrative Rules
      ↓
Agent Workflow
```

The SQL layer produces the authoritative analytical values.

Part 2 validates those values and calculates growth signals.

Part 3 provides controlled narrative templates and validation rules.

Part 4 reuses the Part 2 guardrails and orchestrates the reporting workflow while keeping human approval as the final step.

---

# Project Structure

```text
MEESHO-CAPSTONE
data/
├── generate_dataset.py
├── resellers.csv
├── orders.csv
└── meesho_reseller.db

part1_sql/
├── queries.sql
├── run_queries.py
└── output/
    ├── monthly_category_revenue.csv
    ├── region_revenue_orders.csv
    ├── top_resellers.csv
    ├── zero_order_resellers.csv
    ├── zero_order_count_test.csv
    └── june_delivered_aov.csv

part2_engine/
├── growth_engine.py
├── show_results.py
├── test_growth_engine.py
└── fixtures/
    ├── corrupted_feed.csv
    └── monthly_category_revenue.csv

part3_narrative/
├── masking.py
├── prompt_pack.md
├── narrative_report.md
└── verify_part3.py

part4_agent/
├── agent_spec.md
├── create_fixtures.py
├── mock_agent_runner.py
├── test_mock_agent_runner.py
└── fixtures/
    ├── april.csv
    ├── boundary_current.csv
    ├── boundary_previous.csv
    ├── june.csv
    └── may.csv

README.md
```

---

# Official Documentation Referenced

The following official Python documentation was consulted during implementation:

* Python Standard Library documentation: https://docs.python.org/3/library/
* Python `csv` module documentation: https://docs.python.org/3/library/csv.html
* Python `sqlite3` module documentation: https://docs.python.org/3/library/sqlite3.html
* Python `json` module documentation: https://docs.python.org/3/library/json.html
* pytest documentation: https://docs.pytest.org/

These references were used for implementation and standard-library behavior.
