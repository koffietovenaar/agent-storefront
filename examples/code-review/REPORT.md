# Code review report

Target: `sample_before.py` (32 LOC)  
Scope: correctness, data integrity, and defensive input handling  
Method: manual pattern review plus executable reproduction  
Result: five reproducible findings; all five corrected in `fixed_after.py`

## Findings

### CR-001 — High — Export path can escape the configured directory

- Evidence: `sample_before.py:9`
- Reproduction: `destination_for(base, "../outside.txt")` resolves outside
  `base`.
- Impact: an untrusted filename could direct output to an unintended location.
- Fix: resolve the candidate path and reject it unless it remains relative to
  the resolved base directory.
- Regression test: `test_destination_rejects_parent_traversal`.

### CR-002 — Medium — Mutable default leaks tags between calls

- Evidence: `sample_before.py:12-15`
- Reproduction: two default-argument calls return `["alpha", "beta"]` on the
  second call.
- Impact: unrelated requests can share state and produce incorrect output.
- Fix: default to `None`, then allocate a new list inside the function.
- Regression test: `test_remember_tag_does_not_share_default_state`.

### CR-003 — Medium — Zero totals crash rate calculation

- Evidence: `sample_before.py:20`
- Reproduction: `completion_rate(0, 0)` raises `ZeroDivisionError`.
- Impact: valid empty datasets can terminate a report unexpectedly.
- Fix: validate that `total` is positive and raise a descriptive `ValueError`.
- Regression test: `test_completion_rate_rejects_zero_total`.

### CR-004 — Medium — Negative quantities are accepted

- Evidence: `sample_before.py:25-27`
- Reproduction: `parse_quantity("-2")` returns `-2`.
- Impact: invalid quantities can enter later calculations or storage.
- Fix: reject negative parsed integers with a descriptive `ValueError`.
- Regression test: `test_parse_quantity_rejects_negative_values`.

### CR-005 — Low — CSV fields are not escaped

- Evidence: `sample_before.py:31`
- Reproduction: a value containing a comma creates an ambiguous three-column
  row instead of a two-column row.
- Impact: downstream CSV imports can shift columns and corrupt records.
- Fix: use Python's `csv.writer` rather than joining fields manually.
- Regression test: `test_format_csv_row_escapes_commas`.

## Top risks

1. CR-001 can write outside the intended export directory.
2. CR-002 creates cross-request state contamination.
3. CR-003 makes empty input a crash path.
4. CR-004 permits invalid domain values.
5. CR-005 produces structurally ambiguous data.

## Quick-win checklist

- [x] Constrain resolved output paths to the configured base.
- [x] Replace mutable defaults with per-call allocation.
- [x] Validate divisors before calculating rates.
- [x] Enforce non-negative quantity rules.
- [x] Use the standard CSV serializer.
- [x] Add regression coverage for every corrected behavior.

