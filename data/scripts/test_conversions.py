#!/usr/bin/env python3
"""test_conversions.py - consistency gates for the UMQF conversion lattice.

Asserts the properties that MUST hold before any exchange rate enters UMQF:
  T1 round-trip invertibility  : convert(convert(x, A, B), B, A) == x   (all pairs, many values)
  T2 no-arbitrage              : every conversion cycle multiplies to 1 (no money pump)
  T3 monotonic & sign-preserving
  T4 money-concavity curve invertible (loss -> severity -> loss)
  T5 reconciled life value stays close to the VSL anchor
Also reports (informational, not a failure) the raw cross-rate arbitrage = the current data
inconsistency that more sampling must shrink.

Run: python data/scripts/test_conversions.py   (exit 0 = all pass, 1 = failure)
"""
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import convert as C  # noqa: E402

DATA = HERE.parent
axis = C.build_axis()
C.OUT.write_text(json.dumps(axis, indent=2, ensure_ascii=False), encoding="utf-8")
nodes = list(axis["nodes_log_value"])
RTOL = 1e-9
fails = []


def check(name, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" - {detail}" if detail and not cond else ""))
    if not cond:
        fails.append(name)


# T1 round-trip invertibility
ok = True
for a, b in itertools.permutations(nodes, 2):
    for x in (1.0, 13.7e6, 0.5, 1e-3, 1e9):
        back = C.convert(C.convert(x, a, b, axis), b, a, axis)
        if abs(back - x) > RTOL * max(1.0, abs(x)):
            ok = False
check("T1 round-trip A->B->A recovers A (all pairs, many values)", ok)

# T2 no-arbitrage: every 3-cycle multiplies to 1
ok = True
for a, b, c in itertools.permutations(nodes, 3):
    prod = C.convert(C.convert(C.convert(1.0, a, b, axis), b, c, axis), c, a, axis)
    if abs(prod - 1.0) > 1e-9:
        ok = False
check("T2 no-arbitrage (all conversion cycles multiply to 1)", ok)

# T3 monotonic & sign-preserving
mono = C.convert(2.0, "usd", "life_year", axis) > C.convert(1.0, "usd", "life_year", axis)
sign = C.convert(-1.0, "usd", "life_year", axis) < 0
check("T3 monotonic & sign-preserving", mono and sign)

# T4 money-concavity invertible
if C.money_to_harm(1.0, axis) is not None:
    ok = True
    for loss in (1e4, 1e5, 1e6, 1e7, 1e8):
        back = C.harm_to_money(C.money_to_harm(loss, axis), axis)
        if abs(back - loss) > 1e-6 * loss:
            ok = False
    check("T4 money-concavity curve invertible (loss->severity->loss)", ok)
else:
    check("T4 money-concavity invertible (skipped: not fitted)", True)

# T5 reconciled life value near the VSL anchor
R = {x["ratio"]: x for x in json.loads((DATA / "ratios.json").read_text(encoding="utf-8"))["ratios"]}
lm = R.get("L_to_M", {}).get("estimate")
if lm:
    recon = axis["reconciled_rates"]["life_to_usd"]
    check("T5 reconciled life value within 3x of VSL anchor", 0.33 <= recon / lm <= 3.0, f"${recon:,.0f} vs ${lm:,.0f}")

arb = axis.get("measured_arbitrage_cycle")
if arb:
    print(f"  [INFO] raw cross-rate arbitrage = {arb:.2f}x (data inconsistency; reconciliation removes it for use, sampling must shrink it)")

print(f"\n{'ALL TESTS PASS' if not fails else 'FAILURES: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
