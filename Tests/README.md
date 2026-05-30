# UMQF formula tests

Numerical edge-case tests for the UMQF moral quotient. The formula's single source of
truth is [`../UMQF.md`](../UMQF.md); `umqf.py` mirrors it so we can check that real
situations score the way they should. **A failing test means the formula — or the
test's expectation — needs to be revisited.**

## Run

    python run_tests.py

## Files

- `umqf.py` — reference implementation of `UMQ_base` / `UMQ_final` (keep in sync with `UMQF.md`).
- `cases.json` — the test cases: a plain-language `situation`, the full `args`, and an
  `expected` result with `tolerance` and `reasoning`.
- `run_tests.py` — plugs each case's args into `umqf.py` and compares actual vs expected.

## Adding a case

Append an object to `cases.json`:

    {
      "id": "short_slug",
      "situation": "one or two sentences describing the action and context",
      "args": {"dOS": .., "VSA": .., "Tc": .., "Vc": .., "dSc": .., "Rp": .., "In": ..},
      "expected": {"umq_final": .., "tolerance": 0.02, "label": "..", "reasoning": ".."}
    }

`dSc` (ΔSc) is the increase in suffering the action causes, on `[0, 1]`.

## Scope

These test per-entity `UMQ_base` / `UMQ_final`. Aggregation across entities and the
Complexity Factor (CF) are not yet covered.

## Open issues

- **Pure suffering scores 0.** When `ΔOS = 0` (suffering with no survival change — see
  `immortal_tortured_no_survival_change`), the formula returns 0. Proposed fix and the
  numbers it would give: `proto_suffering_time.py`; design note in `../data/README.md`.
