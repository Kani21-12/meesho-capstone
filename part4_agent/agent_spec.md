# Part 4 — Monitoring Agent Specification

## 4.1 Agent Specification

### Goal

Keep Meesho category managers informed of categories whose month-on-month
revenue moves beyond the 8% threshold, while requiring human approval before
any drafted message can be considered sent.

---

### Tools

The monitoring agent uses the following tools and logic from the previous
parts of the project:

1. `validate_feed` — Part 2
   - Validates the monthly revenue feed before any analysis is performed.
   - The agent must stop if the feed is invalid.

2. `mom_growth` — Part 2
   - Calculates month-on-month revenue growth percentage for each category.

3. `is_flagged` — Part 2
   - Determines whether a category crosses the configured 8% threshold.
   - It can return:
     - `flagged`
     - `not_flagged`
     - `escalate_exact_boundary`

4. Part 3 prompt-pack template-fill logic
   - Creates a narrative message for a flagged category.
   - The message uses only verified values from the project data.
   - No internal reseller identifiers are exposed.

---

### Memory / State

Between runs, the agent needs the previous month's revenue for each category.

This previous-month revenue is required to calculate the next month's
month-on-month growth.

The agent also maintains run-level state containing:

- Current run month
- Previous month
- Validation status
- Validation errors
- Calculated MoM percentages
- Flagged categories
- Suppressed categories
- Escalated categories
- Drafted messages

The agent does not permanently modify the source revenue data.

---

### Planner

The agent follows these ordered subtasks:

1. Load the monthly revenue feed and run `validate_feed`.
2. If the feed is invalid, perform a Hard Stop and report all validation errors.
3. If the feed is valid, calculate `mom_growth` for every category against the
   previous month.
4. Run `is_flagged` for every category.
5. Sort flagged categories by absolute MoM percentage in descending order.
6. Draft a message using the Part 3 template for at most the top 3 flagged
   categories.
7. Log remaining flagged categories beyond the top-3 cap as
   `suppressed, review manually`.
7b. Separately log categories whose `is_flagged` result is
   `escalate_exact_boundary` into `escalated_categories`.
   These categories must not be drafted or silently ignored.
8. Emit one structured JSON object for the run.

---

### Feedback Loop

The agent does not automatically send messages.

Every generated message is drafted and held for human approval.

The runner represents this state using:

`action_taken = "drafted_and_held_for_approval"`

No Gmail, SMTP, API call, or other external message-sending integration is
used in this project.

The human approval checkpoint is the final control before a drafted message
could be considered ready for sending.

---

## Guardrails

### Input Guardrail

`validate_feed` must pass before any other analytical operation runs.

If validation fails:

- No MoM calculation is performed.
- No categories are flagged.
- No messages are drafted.
- The run becomes a Hard Stop.
- All validation errors are surfaced.

---

### Action Guardrail

The agent must never automatically send a message.

It may only:

- identify flagged categories,
- create drafts,
- hold the drafts for human approval.

There is no actual message-sending integration.

The maximum number of drafted messages per run is 3.

This prevents notification flooding when many categories are flagged.

---

### Output Guardrail

Every number appearing in a drafted message must trace back to a verified
Part 1 or Part 2 value.

The agent must not invent revenue, growth percentages, thresholds, dates,
or other numerical values.

Messages must contain the relevant category name and its exact calculated
MoM percentage.

---

## Success and Error Stopping Conditions

### Success Condition

A run succeeds when:

- The input feed passes validation.
- MoM values are calculated successfully.
- Flagged categories are correctly identified.
- At most 3 messages are drafted.
- Additional flagged categories are correctly suppressed.
- Exact-boundary categories are separately escalated.
- Every number in drafted messages is traceable to verified project data.
- The structured JSON output is produced.

A valid run may also produce zero drafts when no category crosses the
threshold.

---

### Error Condition

If `validate_feed` returns `False`, the agent performs a Hard Stop.

The validation errors are surfaced in the output.

No MoM calculation or message drafting is attempted.

The output must contain:

`action_taken = "hard_stop"`

---

## 4.1 Given-When-Then Agent Specifications

### Specification 1 — Valid feed

**Given** a valid monthly revenue feed,

**When** the monitoring agent starts a run,

**Then** it validates the feed successfully and proceeds to MoM analysis.

---

### Specification 2 — Invalid feed

**Given** a monthly revenue feed containing invalid data,

**When** the monitoring agent starts a run,

**Then** it performs a Hard Stop, surfaces the validation errors, and does not
perform MoM calculation or message drafting.

---

### Specification 3 — Flagged category

**Given** a valid feed containing a category whose MoM revenue movement is
beyond the 8% threshold,

**When** the monitoring agent evaluates the category,

**Then** the category is identified as flagged and can be included in the
drafting process subject to the top-3 cap.

---

### Specification 4 — Human approval

**Given** one or more flagged categories with drafted messages,

**When** the monitoring agent completes the drafting process,

**Then** every message is held for human approval and no message is
automatically sent.

---

# Structured JSON Output

Every run must produce exactly one JSON object with these top-level keys:

- `run_month`
- `validation_status`
- `validation_errors`
- `flagged_categories`
- `suppressed_categories`
- `escalated_categories`
- `action_taken`

Each drafted entry in `flagged_categories` contains:

- `category`
- `mom_pct`
- `previous_revenue`
- `current_revenue`
- `drafted`
- `message` when drafted

The `escalated_categories` list contains categories whose
`is_flagged` result is `escalate_exact_boundary`.

The `action_taken` value is either:

- `drafted_and_held_for_approval`
- `hard_stop`